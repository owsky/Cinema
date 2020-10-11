from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    AnonymousUserMixin
from sqlalchemy import create_engine, MetaData, Table, Column, Float, Integer, String, DateTime, Boolean, select
import secrets

from sqlalchemy.sql.functions import user

app = Flask(__name__)

# DB connection
engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')
metadata = MetaData(engine)

actors = Table('actors', metadata,
               Column('actors_id', Integer, primary_key=True),
               Column('actors_fullname', String),
               )
cast = Table('cast', metadata,
             Column('cast_id', Integer, primary_key=True),
             Column('cast_movie', Integer),
             Column('cast_actor', Integer)
             )
movies = Table('movies', metadata,
               Column('movies_id', Integer, primary_key=True),
               Column('movies_title', String),
               Column('movies_duration', Integer),
               Column('movies_genre', String),
               Column('movies_synopsis', String),
               Column('movies_director', String)  # Tabella separata?
               )
rooms = Table('rooms', metadata,
              Column('rooms_id', Integer, primary_key=True),
              Column('rooms_name', String)
              )
seats = Table('seats', metadata,
              Column('seats_id', Integer, primary_key=True),
              Column('seats_name', String),
              Column('seats_room', Integer)
              )
tickets = Table('tickets', metadata,
                Column('tickets_id', Integer, primary_key=True),
                Column('tickets_user', Integer),
                Column('tickets_projection', Integer),
                Column('tickets_seat', Integer)
                )
users = Table('users', metadata,
              Column('users_id', Integer, primary_key=True),
              Column('users_email', String),
              Column('users_name', String),
              Column('users_surname', String),
              Column('users_pwd', String),
              Column('users_is_manager', Boolean)
              )
projections = Table('projections', metadata,
                    Column('projections_id', Integer, primary_key=True),
                    Column('projections_movie', Integer),
                    Column('projections_date_time', DateTime),
                    Column('projections_room', Integer),
                    Column('projections_price', Float),
                    Column('projections_remain', Integer))

# Login Manager
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id, email, name, surname, pwd, is_manager):
        self.id = user_id
        self.email = email
        self.name = name
        self.surname = surname
        self.pwd = pwd
        self.is_manager = is_manager

    def is_manager(self):
        return self.is_manager

    def get_name(self):
        return self.name


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = None
        self.is_manager = False


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
@app.route('/')
def home():
    return render_template("index.html", films=get_movies(), name=User.get_name(current_user),
                           manager=User.is_manager(current_user))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(select([users]).where(users.c.users_email == request.form['user']))
        u = rs.fetchone()
        conn.close()
        if u and request.form['pass'] == u.users_pwd:
            u = user_by_email(request.form['user'])
            login_user(u, remember=True)
            return redirect(url_for('home'))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        conn = engine.connect()
        ins = users.insert()
        conn.execute(ins, [
            {"users_name": request.form['name'], "users_surname": request.form['surname'],
             "users_email": request.form['email'], "users_pwd": request.form['pwd'], "users_is_manager": False}
        ])
        conn.close()
        return redirect(url_for('home'))
    return render_template("signup.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


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


def get_movies():
    conn = engine.connect()
    rs = conn.execute(select([movies]))
    films = rs.fetchall()
    conn.close()
    return films


def get_projections():
    conn = engine.connect()
    rs = conn.execute(select([projections]))
    proj = rs.fetchall()
    conn.close()
    return proj


if __name__ == '__main__':
    app.run()
