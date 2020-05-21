from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, select
import secrets

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# DB
engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')
metadata = MetaData(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
db = SQLAlchemy(app)

actors = Table('actors', metadata,
               Column('actors_id', Integer, primary_key=True),
               Column('actors_name', String),
               Column('actors_surname', String)
               )
cast = Table('cast', metadata,
             Column('cast_id', Integer, primary_key=True),
             Column('cast_movie', Integer),
             Column('cast_actor', Integer)
             )
movies = Table('movies', metadata,
               Column('movies_id', Integer, primary_key=True),
               Column('movies_title', String),
               Column('movies_genre', String),
               Column('movies_synopsis', String),
               Column('movies_director', String)
               )
rooms = Table('rooms', metadata,
              Column('rooms_id', Integer, primary_key=True),
              Column('rooms_name', String)
              )
seats = Table('seats', metadata,
              Column('seats_id', Integer, primary_key=True),
              Column('seats_room', Integer)
              )
tickets = Table('tickets', metadata,
                Column('tickets_id', Integer, primary_key=True),
                Column('tickets_user', Integer),
                Column('tickets_movie', Integer),
                Column('tickets_seat', Integer),
                Column('tickets_date_time', DateTime)
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
                    Column('projections_room', Integer))

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


"""Session = sessionmaker(bind=engine)
session = Session()
user = User()
user.id
session.add(User(request.form['id'],
                 request.form['email'],
                 request.form['name'],
                 request.form['surname'],
                 request.form['pwd'],
                 False))
session.commit()
session.close()
print("SUCCESSO")
"""


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute(select([users]).where(users.c.users_id == user_id))
    user = rs.fetchone()
    conn.close()
    return User(user.users_id, user.users_email, user.users_name, user.users_surname, user.users_pwd, user.users_is_manager)


# App routes
@app.route('/')
def home():
    return render_template("index.html", films=get_movies())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()

        rs = conn.execute(select([users]).where(users.c.users_email == request.form['user']))

        u = rs.fetchone()
        conn.close()
        if u and request.form['pass'] == u.users_pwd:
            user = user_by_email(request.form['user'])
            login_user(user)
            return render_template("private.html", manager=user.is_manager, films=get_movies())
        else:
            return render_template("login.html", wrong=True)
    else:
        return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        conn = engine.connect()
        conn.execute("INSERT INTO users VALUES (3,%s,'huang','ruoxin',%s,False)", request.form['user'],
                     request.form['pass'])
        conn.close()
        return render_template("login.html")
    else:
        return render_template("index.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Functions
def user_by_email(user_email):
    conn = engine.connect()
    rs = conn.execute(select([users]).where(users.c.users_email == user_email))
    user = rs.fetchone()
    conn.close()
    return User(user.users_id, user.users_email, user.users_name, user.users_surname, user.users_pwd, user.users_is_manager)


def get_movies():
    conn = engine.connect()
    rs = conn.execute(select([movies]))
    films = rs.fetchall()
    conn.close()
    return films


if __name__ == '__main__':
    app.run()
