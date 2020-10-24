from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    AnonymousUserMixin
from sqlalchemy import select, text, insert
from flask_wtf import FlaskForm
from wtforms import SelectField
import secrets
from schema import engine, actors, cast, directors, movies, rooms, seats, tickets, users, projections

app = Flask(__name__)


# Login Manager
class User(UserMixin):
    def __init__(self, user_id, email, name, surname, pwd, is_manager):
        self.id = user_id
        self.email = email
        self.name = name
        self.surname = surname
        self.pwd = pwd
        self.is_manager = is_manager


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = None
        self.is_manager = False


class Projection:
    def __init__(self, proj_id, date, time, room, price, tickets_left):
        self.id = proj_id
        self.date = date
        self.time = time
        self.room = room
        self.price = price
        self.tickets_left = tickets_left


class Director:
    def __init__(self, direct_id, name):
        self.id = direct_id
        self.name = name


app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute(select([users]).where(users.c.users_id == user_id))
    u = rs.fetchone()
    conn.close()
    return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd, u.users_is_manager)


# App routes
# User side
@app.route('/')
def home():
    return render_template("user/index.html", films=get_last_movies())


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['surname'] or not request.form['email'] or not request.form['pwd']:
            flash("Missing information")
        if user_by_email(request.form['email']):
            flash("There's already an account set up to use this email address")
        else:
            conn = engine.connect()
            ins = users.insert()
            conn.execute(ins, [
                {"users_name": request.form['name'], "users_surname": request.form['surname'],
                 "users_email": request.form['email'], "users_pwd": request.form['pwd'], "users_is_manager": False}
            ])
            conn.close()
            return redirect(url_for('home'))
    return render_template("user/signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(select([users]).where(users.c.users_email == request.form['user']))
        u = rs.fetchone()
        conn.close()
        if u and request.form['pass'] == u.users_pwd:
            u = user_by_email(request.form['user'])
            login_user(u)
            return redirect(url_for('home'))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))
    else:
        return render_template("user/login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/projections')
def projections():
    return render_template("user/projections.html", projections=get_projections(None))


@app.route('/movies')
def movies_route():
    return render_template("movies.html", movies=get_movies(None))


@app.route('/<title>', methods=['GET', 'POST'])
def movie_info(title):
    m = get_movies(title)
    if not m:
        abort(404)
    proj = get_projections(title)
    if request.method == 'POST':
        if reserve_ticket(request.form.get('proj')):
            flash("Ticket reserved successfully")
        else:
            flash("Failed to reserve ticket")
    return render_template("user/movie_info.html", movie=m, projections=format_projections(proj),
                           cast=get_actors(title))


# Manager side
@app.route('/manager/')
@login_required
def movie_manager():
    if not current_user.is_manager:
        abort(403)
    else:
        conn = engine.connect()
        s = text("SELECT * FROM public.projections JOIN public.movies ON (projections_movie=movies_id)")
        rs = conn.execute(s)
        u = rs.fetchall()
        conn.close()
        for p in u:
            date = p.projections_date_time.strftime("%m/%d/%Y")
            hour = p.projections_date_time.strftime("%H:%M:%S")[:5]
            return render_template("manager/manager.html", projection=u, date=date, hour=hour)


# Update
@app.route('/update_movie/<title>', methods=['GET', 'POST'])
@login_required
def update_movie(title):
    if not current_user.is_manager:
        abort(403)
    m = get_movies(title)
    d = get_directors_by_id(m.movies_director)
    if request.method == 'POST':
        conn = engine.connect()
        director = get_directors_by_name(request.form['director'])
        new_title = request.form['title']
        genre = request.form['genre']
        duration = request.form['duration']
        synopsis = request.form['synopsis']
        s = text("UPDATE movies SET movies_title= :t, movies_genre=:g, movies_duration=:d, movies_synopsis=:s, "
                 "movies_director=:dr WHERE movies_id =:cod")
        conn.execute(s, t=new_title, g=genre, d=duration, s=synopsis, dr=director.directors_id, cod=m.movies_id)
        conn.close()
        return render_template('manager/movie_manager.html')
    return render_template('manager/update_movie.html', movie_to_update=m, direct=d)


@app.route('/update_movie/<title>', methods=['GET', 'POST'])
@login_required
def update_projection(title):
    if not current_user.is_manager:
        abort(403)
    m = get_movies(title)
    r = get_rooms_by_name(get_projections(title).projections_room)
    if request.method == 'POST':
        conn = engine.connect()
        time = request.form['date_time']
        room = get_rooms_by_name(request.form['room'])
        price = request.form['price']
        s = text("UPDATE projections SET projections_date_time= :t, projections_room=:r, projections_price=:p WHERE "
                 "projections_movie =:cod")
        conn.execute(s, t=time, r=room.rooms_id, p=price, cod=m.movies_id)
        conn.close()
        return render_template('manager/movie_manager.html')
    return render_template('manager/update_movie.html', movie=m, room=r)


class Form(FlaskForm):
    director = SelectField('director', choices=[])


# Add
@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        conn = engine.connect()
        ins = movies.insert()
        director = get_directors_by_name(request.form['director'])
        # TODO
        conn.execute(ins, [
            {"movies_title": request.form['title'], "movies_genre": request.form['genre'],
             "movies_duration": request.form['duration'], "movies_synopsis": request.form['synopsis'],
             "movies_director": director.directors_id,
             "movies_date": request.form['date']}])
        conn.close()
        return render_template("manager/movie_manager.html")
    print(get_genres())
    return render_template("manager/add_movie.html", gen=get_genres())


@app.route('/session_manager')
@login_required
def session_manager():
    if not current_user.is_manager:
        abort(403)
    return render_template("manager/update_projection.html", movies=get_projections(None))


@app.route('/add_projection', methods=['GET', 'POST'])
@login_required
def add_projection():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        conn = engine.connect()
        if not get_movies(request.form['title']):
            flash("This movie has not been added!")
            return render_template("manager/add_projection.html")
        else:
            ins = projections.insert()
            conn.execute(ins, [
                {"projections_movie": request.form['title'], "projections_date_time": request.form['date_time'],
                 "projections_room": get_rooms_by_name(request.form['room']).rooms_id,
                 "projections_price": request.form['price']}])
            conn.close()
            return render_template("manager/update_projection.html", movies=get_projections(None))
    else:
        return render_template("manager/add_projection.html")


# Delete
@app.route('/delete_movie/<title>')
@login_required
def delete_movie(title):
    if not current_user.is_manager:
        abort(403)
    conn = engine.connect()
    s = text("DELETE FROM public.movies WHERE movies_title = :mt")
    conn.execute(s, mt=title)
    conn.close()
    return redirect(url_for('movies_route'))


@app.route('/delete_projection/<title>')
@login_required
def delete_projection(title):
    if not current_user.is_manager:
        abort(403)
    conn = engine.connect()
    p = get_projections(title)
    s = text("DELETE FROM public.projections WHERE projections_movie = :m AND projections_date_time = :t")
    conn.execute(s, m=p.projections_movie, t=p.projections_date_time)
    # TODO
    conn.close()
    return redirect(url_for('projections'))


# Functions
def get_actors_by_name(name):
    conn = engine.conn()
    s = text("SELECT * FROM actors WHERE actors_fullname = :n")
    rs = conn.execute(s, n=name)
    act = rs.fetchone
    conn.close()
    return act


def get_rooms_by_name(name):
    conn = engine.connect()
    s = text("SELECT * FROM rooms WHERE rooms_name = :n")
    rs = conn.execute(s, n=name)
    rid = rs.fetchone()
    conn.close()
    return rid


def get_rooms_by_id(cod):
    conn = engine.connect()
    s = text("SELECT * FROM rooms WHERE rooms_id = :c")
    rs = conn.execute(s, c=cod)
    rid = rs.fetchone()
    conn.close()
    return rid


def get_directors_by_id(cod):
    conn = engine.connect()
    if cod:
        s = text("SELECT * FROM directors WHERE directors_id = :c")
        rs = conn.execute(s, c=cod)
        did = rs.fetchone()
    else:
        s = text("SELECT * FROM directors")
        rs = conn.execute()
        did = rs.fetchall()
    conn.close()
    return did


def get_directors_by_name(name):
    conn = engine.connect()
    if name:
        s = text("SELECT * FROM directors WHERE directors_name = :n")
        rs = conn.execute(s, n=name)
        did = rs.fetchone()
    else:
        s = text("SELECT * FROM directors")
        rs = conn.execute()
        did = rs.fetchall()
    conn.close()
    return did


# Functions
def user_by_email(user_email):
    conn = engine.connect()
    rs = conn.execute(select([users]).where(users.c.users_email == user_email))
    u = rs.fetchone()
    conn.close()
    if u:
        return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd, u.users_is_manager)
    else:
        return None


def get_movies(mov):
    conn = engine.connect()
    if mov:
        s = text("""SELECT * FROM movies
                    JOIN directors ON movies.movies_director = directors.directors_id
                    WHERE movies_title = :e1""")
        rs = conn.execute(s, e1=mov)
        films = rs.fetchone()
    else:
        s = text("SELECT * FROM movies JOIN directors ON movies_director = directors_id")
        rs = conn.execute(s)
        films = rs.fetchall()
    conn.close()
    return films


def get_actors(mov):
    conn = engine.connect()
    s = text("""SELECT actors_fullname FROM movies
                JOIN directors ON movies.movies_director = directors.directors_id
                JOIN public.cast ON movies_id = public.cast.cast_movie
                JOIN actors ON cast_actor = actors_id
                WHERE movies_title = :e1""")
    rs = conn.execute(s, e1=mov)
    act = rs.fetchall()
    conn.close()
    return act


def get_last_movies():
    conn = engine.connect()
    s = text("SELECT * FROM movies JOIN directors ON movies_director = directors_id ORDER BY movies_id DESC LIMIT 5")
    rs = conn.execute(s)
    films = rs.fetchall()
    conn.close()
    return films


def get_projections(mov):
    conn = engine.connect()
    if mov:
        s = text("SELECT * FROM public.projections JOIN public.movies ON projections_movie = movies_id JOIN "
                 "public.cast ON movies_id = cast_movie JOIN public.actors ON cast_actor = actors_id JOIN "
                 "public.directors ON movies_director = directors_id JOIN public.rooms ON projections_room = rooms_id "
                 "WHERE movies_title = :e1 AND projections_date_time >= current_date")
        rs = conn.execute(s, e1=mov)
    else:
        s = text("SELECT * FROM public.projections JOIN public.movies ON projections_movie = movies_id JOIN "
                 "public.cast ON movies_id = cast_movie JOIN public.actors ON cast_actor = actors_id JOIN "
                 "public.directors ON movies_director = directors_id JOIN public.rooms ON projections_room = rooms_id "
                 "WHERE projections_date_time >= current_date")
        rs = conn.execute(s)
    proj = rs.fetchall()
    conn.close()
    return proj


def how_many_seats_left(proj_id):
    conn = engine.connect()
    s1 = text("""SELECT COUNT(seats_id) FROM public.projections, public.movies, public.rooms, public.seats
                 WHERE projections_movie = movies_id AND projections_room = rooms_id AND seats_room = rooms_id
                 AND projections_id = :e1""")
    rs1 = conn.execute(s1, e1=proj_id)
    total = rs1.fetchone()
    s2 = text("""SELECT COUNT(tickets_id) FROM public.projections, public.tickets
                 WHERE tickets_projection = projections_id AND projections_id = :e1""")
    rs2 = conn.execute(s2, e1=proj_id)
    sold = rs2.fetchone()
    return total[0] - sold[0]


def reserve_ticket(proj_id):
    conn = engine.connect()
    if how_many_seats_left(proj_id) == 0:
        return False
    else:
        s1 = text("""SELECT COUNT(tickets_id) FROM public.projections, public.tickets
                         WHERE tickets_projection = projections_id AND projections_id = :e1""")
        rs1 = conn.execute(s1, e1=proj_id)
        sold = rs1.fetchone()

        s2 = text("INSERT INTO public.tickets(tickets_user, tickets_projection, tickets_seat) VALUES (:e1, :e2, :e3)")
        conn.execute(s2, e1=current_user.id, e2=proj_id, e3=sold[0] + 1)
        return True


def format_projections(proj):
    proj_list = list()
    for p in proj:
        date = p.projections_date_time.strftime("%m/%d/%Y")
        hour = p.projections_date_time.strftime("%H:%M:%S")[:5]
        proj_list.append(
            Projection(p.projections_id, date, hour, p.rooms_name, p.projections_price, how_many_seats_left(p[0])))
    return proj_list


def get_genres():
    conn = engine.connect()
    s = text("SELECT unnest(enum_range(NULL::public.genre)) AS genre")
    rs = conn.execute(s)
    gen = rs.fetchall()
    return gen


if __name__ == '__main__':
    app.run(debug=True)
