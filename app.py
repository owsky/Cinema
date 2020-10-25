from flask import Flask, render_template, request, redirect, url_for, abort, flash
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    AnonymousUserMixin
from sqlalchemy import select, text
import secrets
from schema import engine, users, projections

app = Flask(__name__)


# Login Manager
class User(UserMixin):
    def __init__(self, user_id, email, name, surname, pwd, is_manager, balance):
        self.id = user_id
        self.email = email
        self.name = name
        self.surname = surname
        self.pwd = pwd
        self.is_manager = is_manager
        self.balance = balance


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
    return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd, u.users_is_manager,
                u.users_balance)


# App routes
# User side
@app.route('/')
def home():
    return render_template("user/index.html", films=get_last_movies())


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['surname'] or not request.form['email'] \
                or not request.form['pwd']:
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


@app.route('/profile')
@login_required
def profile():
    return render_template("user/profile.html", info=get_orders(current_user.id))


@app.route('/projections')
def projections():
    return render_template("user/projections.html", projections=get_projections(None))


@app.route('/movies')
def movies_route():
    return render_template("movies.html", movies=get_movies(None))


@app.route('/<title>')
def movie_info(title):
    m = get_movies(title)
    if not m:
        abort(404)
    proj = get_projections(title)
    return render_template("user/movie_info.html", movie=m, projections=format_projections(proj),
                           cast=get_actors(title))


@app.route('/<title>/<projection>', methods=['GET', 'POST'])
@login_required
def purchase_ticket(title, projection):
    m = get_movies(title)
    if not m:
        abort(404)
    if request.method == 'POST':
        if purchase(projection, request.form.getlist('seat')):
            flash("Successfully purchased seats: " + ', '.join(request.form.getlist('seat')))
        else:
            flash("Error")
    return render_template("user/purchase.html", seats=free_seats(projection), mov=m.movies_title, proj=projection)


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
        genre = request.form['genre']
        duration = request.form['duration']
        synopsis = request.form['synopsis']
        s = text("UPDATE movies SET movies_genre=:g, movies_duration=:d, movies_synopsis=:s, "
                 "movies_director=:dr WHERE movies_id =:cod")
        conn.execute(s, g=genre, d=duration, s=synopsis, dr=director.directors_id, cod=m.movies_id)
        conn.close()
        return render_template('manager/movie_manager.html')
    return render_template('manager/update_movie.html', movie_to_update=m, direct=d, gen=get_genres(), dir=get_directors_by_name(None),c=get_actors(title))


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
        # director = get_directors_by_name(request.form['director'])
        return render_template('movies.html')
    return render_template('manager/update_projections.html', movie=m, room=r)


# (Manager) aggiungere un film
@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        conn = engine.connect()
        title = request.form['title']
<<<<<<< HEAD
        # controllo che non ci sia già il film
        if get_movies(title) is not None:
            flash("This movie has already been added")
            return redirect(url_for('add_movie'))
        else:
            genre = request.form['genre']
            duration = request.form['duration']
            synopsis = request.form['synopsis']
            date = request.form['day']
            director = get_directors_by_name(request.form['director'])

            # inserisco il film nel DB
            s = text("INSERT INTO movies (movies_title, movies_genre, movies_duration, movies_synopsis, movies_date, "
                     "movies_director) VALUES (:t, :g, :d, :s, :dt, :dr)")
            conn.execute(s, t=title, g=genre, d=duration, s=synopsis, dt=date, dr=director.directors_id)
            conn.close()
            flash("Movie added successfully!")
            return redirect(url_for('movies_route'))
    return render_template("manager/add_movie.html", gen=get_genres(), dir=get_directors_by_name(None))


# (Manager) aggiungere una proiezione controllando con un trigger che non sia stata il range di tempo non sia stato
# occupato da altre proiezioni.
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
        return render_template("manager/add_projection.html", mov=get_movies(None), room=get_rooms_by_id(None))
=======
        genre = request.form['genre']
        duration = request.form['duration']
        synopsis = request.form['synopsis']
        date = request.form['day']
        director = get_directors_by_name(request.form['director'])
        act = request.form['actors']
        act_list = act.split(',' or ', ')
        addact = text("INSERT INTO actors (actors_fullname) VALUES (:n)")
        for li in act_list:
            conn.execute(addact, n=li)
        s = text("INSERT INTO movies (movies_title, movies_genre, movies_duration, movies_synopsis, movies_date, "
                 "movies_director) VALUES (:t, :g, :d, :s, :dt, :dr)")
        conn.execute(s, t=title, g=genre, d=duration, s=synopsis, dt=date, dr=director.directors_id)
        conn.close()
        flash("Movie added successfully!")
        return render_template("movies.html")
    print(get_genres())
    return render_template("manager/add_movie.html", gen=get_genres())
>>>>>>> fd28f962039e3a9f8374fcde82720e9ceb16e30b


# (Manager) aggiungere un regista nel caso non è tra le scelte possibili (non è già presente nel DB)
@app.route('/add_director', methods=['GET', 'POST'])
@login_required
def add_director():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        if get_directors_by_name(request.form['name']) is not None:
            flash("Director has already been added")
        else:
            conn = engine.connect()
            name = request.form['name']
            s = text("INSERT INTO directors (directors_name) VALUES (:n)")
            conn.execute(s, n=name)
            conn.close()
            return redirect(url_for('add_movie'))
    return render_template("manager/add_director.html")


# (Manager) connettere attori a un film (uno alla volta)
@app.route('/<title>/add_actor', methods=['GET', 'POST'])
@login_required
def add_actor(title):
    if not current_user.is_manager:
        abort(403)
    m = get_movies(title)
    if request.method == 'POST':
        conn = engine.connect()
        actor = request.form['actor']
        # aggiungo l'attore se non c'era già nel DB
        if get_actors_by_name(actor) is None:
            addact = text("INSERT INTO actors(actors_fullname) VALUES (:a)")
            conn.execute(addact, a=actor)
        a = get_actors_by_name(actor)
        # connetto gli attori al film corrispondente inserendoli nel cast
        if check_cast(m.movies_id, a.actors_id) is None:
            addcast = text("INSERT INTO public.cast(cast_movie, cast_actor) VALUES (:m, :a)")
            conn.execute(addcast, m=m.movies_id, a=get_actors_by_name(actor).actors_id)
            flash("Actor added successfully!")
        else:
            flash("Actor has already been added!")
        conn.close()
        return redirect(url_for('movies_route'))
    return render_template('manager/add_actor.html', movie_to_update=m)


# statistiche
@app.route('/show_echarts')
@login_required
def show_echarts():
    if not current_user.is_manager:
        abort(403)
    bar = get_bar()
    pie = get_pie()
    return render_template("manager/show_echarts.html", bar_options=bar.dump_options(), pie_options=pie.dump_options())



# grafico a linee: può non essere inserita
def get_line() -> Line:
    conn = engine.connect()
    s = text("SELECT movies_genre AS genre, SUM(CASE WHEN (tickets_id IS NOT NULL) THEN 1 ELSE 0 END) AS sum FROM "
             "tickets LEFT JOIN projections on tickets_projection = projections_id LEFT JOIN movies on "
             "projections_movie = movies_id GROUP BY movies_genre")
    datas = conn.execute(s).fetchall()
    conn.close()
    c = (
        Line().add_xaxis([data['genre'] for data in datas]).add_yaxis("Quantity", [data['sum'] for data in datas]).set_global_opts(title_opts=opts.TitleOpts(title="Genre"))
    )
    return c


# grafico a barre: seleziona i film in base ai biglietti venduti
def get_bar() -> Bar:
    conn = engine.connect()
    s = text("SELECT movies_id AS id, SUM(CASE WHEN (tickets_id IS NOT NULL) THEN 1 ELSE 0 END) AS sum FROM "
             "tickets LEFT JOIN projections on tickets_projection = projections_id LEFT JOIN movies on "
             "projections_movie = movies_id GROUP BY movies_id, movies_title")
    datas = conn.execute(s).fetchall()
    conn.close()
    c = (
        Bar().add_xaxis([data['id'] for data in datas]).add_yaxis("Quantity", [data['sum'] for data in datas]).set_global_opts(title_opts=opts.TitleOpts(title="Movies"))
    )
    return c


# grafico a cerchio: seleziona i generi più preferiti dalle persone
def get_pie() -> Pie:
    conn = engine.connect()
    s = text("SELECT movies_genre AS genre, SUM(CASE WHEN (tickets_id IS NOT NULL) THEN 1 ELSE 0 END) AS sum FROM "
             "tickets LEFT JOIN projections on tickets_projection = projections_id LEFT JOIN movies on "
             "projections_movie = movies_id GROUP BY movies_genre")
    datas = conn.execute(s).fetchall()
    conn.close()
    c = (
        Pie().add("", [(data['genre'], data['sum']) for data in datas]).set_global_opts(title_opts=opts.TitleOpts(title="Genres")).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


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
    conn = engine.connect()
    s = text("SELECT * FROM actors WHERE actors_fullname = :n")
    rs = conn.execute(s, n=name)
    act = rs.fetchone()
    conn.close()
    return act


def get_rooms_by_name(name):
    conn = engine.connect()
    if name:
        s = text("SELECT * FROM rooms WHERE rooms_name = :n")
        rs = conn.execute(s, n=name)
        rid = rs.fetchone()
    else:
        s = text("SELECT * FROM rooms")
        rs = conn.execute(s)
        rid = rs.fetchall()
    conn.close()
    return rid


def get_rooms_by_id(cod):
    conn = engine.connect()
    if cod:
        s = text("SELECT * FROM rooms WHERE rooms_id = :c")
        rs = conn.execute(s, c=cod)
        rid = rs.fetchone()
    else:
        s = text("SELECT * FROM rooms")
        rs = conn.execute(s)
        rid = rs.fetchall()
    conn.close()
    return rid


def check_cast(movid,actid):
    conn = engine.connect()
    s = text("SELECT * FROM public.cast WHERE cast_actor=:a AND cast_movie=:m")
    rs = conn.execute(s, a=actid, m=movid)
    check = rs.fetchone()
    conn.close()
    return check


def get_directors_by_id(cod):
    conn = engine.connect()
    if cod:
        s = text("SELECT * FROM directors WHERE directors_id = :c")
        rs = conn.execute(s, c=cod)
        did = rs.fetchone()
    else:
        s = text("SELECT * FROM directors")
        rs = conn.execute(s)
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
        rs = conn.execute(s)
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
        return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd, u.users_is_manager,
                    u.users_balance)
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
    s = text("""SELECT COUNT(seats_id) as s
                     FROM seats
                     WHERE seats_id NOT IN (
                        SELECT seats_id
                        FROM public.projections
                        JOIN public.tickets ON tickets_projection = projections_id
                        JOIN public.seats ON tickets_seat = seats_id
                        WHERE projections_id = :e1)""")
    rs = conn.execute(s, e1=proj_id)
    f = rs.fetchone()
    return f.s


def free_seats(proj_id):
    conn = engine.connect()
    s = text("""SELECT *
                 FROM seats
                 WHERE seats_id NOT IN (
                    SELECT seats_id
                    FROM public.projections
                    JOIN public.tickets ON tickets_projection = projections_id
                    JOIN public.seats ON tickets_seat = seats_id
                    WHERE projections_id = :e1)""")
    rs = conn.execute(s, e1=proj_id)
    f = rs.fetchall()
    return f


def purchase(proj_id, selected_seats):
    with engine.begin() as connection:
        s1 = text("SELECT users_balance FROM public.users WHERE users_id = :e1")
        rs1 = connection.execute(s1, e1=current_user.id)
        balance = rs1.fetchone()

        s2 = text("SELECT projections_price FROM public.projections WHERE projections_id = :e2")
        rs2 = connection.execute(s2, e2=proj_id)
        tprice = rs2.fetchone()
        total = balance.users_balance - (tprice.projections_price * len(selected_seats))
        if total < 0:
            return False

        for x in selected_seats:
            s = text(
                "INSERT INTO public.tickets(tickets_user, tickets_projection, tickets_seat) VALUES (:e1, :e2, :e3)")
            connection.execute(s, e1=current_user.id, e2=proj_id, e3=x)
        s = text("UPDATE public.users SET users_balance = :e1 WHERE users_id = :e2")
        connection.execute(s, e1=total, e2=current_user.id)
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


def get_orders(uid):
    conn = engine.connect()
    s = text("""SELECT movies_title, projections_date_time, rooms_name, seats_name FROM tickets
                JOIN seats ON seats_id=tickets_seat
                JOIN rooms ON rooms_id=seats_room
                JOIN projections ON tickets_projection=projections_id
                JOIN movies ON movies_id=projections_movie
                WHERE tickets_user=:e1""")
    rs = conn.execute(s, e1=uid)
    orders = rs.fetchall()
    return orders


if __name__ == '__main__':
    app.run(debug=True)
