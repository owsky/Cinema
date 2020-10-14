from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    AnonymousUserMixin
from sqlalchemy import select, text
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
    return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd,
                u.users_is_manager)


# App routes
# User side
@app.route('/')
def home():
    return render_template("index.html", films=get_movies(None))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if user_by_email(request.form['email']) is not None:
            flash("There’s already an account set up to use this email address")
        else:
            conn = engine.connect()
            ins = users.insert()
            conn.execute(ins, [
                {"users_name": request.form['name'], "users_surname": request.form['surname'],
                 "users_email": request.form['email'], "users_pwd": request.form['pwd'], "users_is_manager": False}
            ])
            conn.close()
            return redirect(url_for('home'))
    return render_template("signup.html")


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
        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/projections')
def projections():
    return render_template("projections.html", projections=get_projections())


@app.route('/<title>')
def movie_info(title):
    m = get_movies(title)
    if m is None:
        abort(404)
    return render_template("movie_info.html", movie=m)


# Manager side
@app.route('/movie_manager')
@login_required
def movie_manager():
    if not current_user.is_manager:
        abort(403)
    return render_template("movie_manager.html")


@app.route('/movie_manager/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_manager:
        abort(403)

    if request.method == 'POST':
        conn = engine.connect()
        ins = movies.insert()
        conn.execute(ins, [
            {"movies_title": request.form['title'], "movies_genre": request.form['genre'],
             "movies_synopsis": request.form['synopsis'], "movies_director": request.form['director']}
        ])
        conn.close()
        return render_template("movie_manager.html", movies=get_projections())
    else:
        return render_template("add_movie.html")


@app.route('/session_manager')
@login_required
def session_manager():
    if not current_user.is_manager:
        abort(403)
    return render_template("session_manager.html", movies=get_projections())


@app.route('/session_manager/add_session', methods=['GET', 'POST'])
@login_required
def add_session():
    if not current_user.is_manager:
        abort(403)

    if request.method == 'POST':
        conn = engine.connect()
        ins = projections.insert()
        conn.execute(ins, [
            {"projections_movie": request.form['movie'], "projections_date_time": request.form['date'],
             "projections_room": request.form['room'], "projections_price": request.form['price'],
             "projections_remain": request.form['capacity']}
        ])
        conn.close()
        return render_template("session_manager.html", movies=get_projections())
    else:
        return render_template("add_session.html")


@login_required
def delete_movie():
    if not current_user.is_manager:
        abort(403)
        '''TODO'''


# Functions
def user_by_email(user_email):
    conn = engine.connect()
    rs = conn.execute(select([users]).where(users.c.users_email == user_email))
    u = rs.fetchone()
    conn.close()
    return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd,
                u.users_is_manager)


def get_movies(mov):
    conn = engine.connect()
    if mov:
        s = text("SELECT * FROM movies, directors WHERE movies_director = directors_id AND movies_title = :e1")
        rs = conn.execute(s, e1=mov)
        films = rs.fetchone()
    else:
        rs = conn.execute(select([movies, directors]).where(movies.c.movies_director == directors.c.directors_id))
        films = rs.fetchall()
    conn.close()
    return films


def get_projections():
    conn = engine.connect()
    s = text("""SELECT * FROM public.projections, public.movies, public.cast, public.actors, public.directors, public.rooms
            WHERE projections_movie = movies_id AND movies_director = directors_id AND movies_id = cast_movie
            AND cast_movie = actors_id AND projections_room = rooms_id""")
    rs = conn.execute(s)
    proj = rs.fetchall()
    conn.close()
    return proj


if __name__ == '__main__':
    app.run(debug=True)
