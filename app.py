from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, select
import secrets

app = Flask(__name__)

# DB
engine = create_engine('postgresql://postgres:toor@localhost/cinema')
metadata = MetaData(engine)

actors = Table('actors', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String),
               Column('surname', String)
               )
cast = Table('cast', metadata,
             Column('id', Integer, primary_key=True),
             Column('movie', Integer),
             Column('actor', Integer)
             )
movies = Table('movies', metadata,
               Column('id', Integer, primary_key=True),
               Column('title', String),
               Column('genre', String),
               Column('synopsis', String),
               Column('director', String)
               )
rooms = Table('rooms', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String)
              )
seats = Table('seats', metadata,
              Column('id', Integer, primary_key=True),
              Column('room', Integer)
              )
tickets = Table('tickets', metadata,
                Column('id', Integer, primary_key=True),
                Column('user', Integer),
                Column('movie', Integer),
                Column('seat', Integer),
                Column('date_time', DateTime)
                )
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('email', String),
              Column('name', String),
              Column('surname', String),
              Column('pwd', String),
              Column('is_manager', Boolean)
              )

# Login Manager
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, email, name, surname, pwd, is_manager):
        self.id = id
        self.email = email
        self.name = name
        self.surname = surname
        self.pwd = pwd
        self.is_manager = is_manager


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute(select([users]).where(users.c.id == user_id))
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.name, user.surname, user.pwd, user.is_manager)


# Actual app
@app.route('/')
def home():
    # The home lists all the currently available movies
    conn = engine.connect()
    rs = conn.execute(select([movies]))
    f = rs.fetchall()
    conn.close()
    return render_template("index.html", films=f)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/check-login', methods=['GET', 'POST'])
def check_login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute(select([users]).where(users.c.email == request.form['user']))
        u = rs.fetchone()
        conn.close()
        if u and request.form['pass'] == u.pwd:
            user = user_by_email(request.form['user'])
            login_user(user)
            return render_template("private.html", manager=user.is_manager)
    return render_template("login.html", wrong=True)


def user_by_email(user_email):
    conn = engine.connect()
    rs = conn.execute(select([users]).where(users.c.email == user_email))
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.name, user.surname, user.pwd, user.is_manager)


@app.route('/private')
@login_required
def private():
    conn = engine.connect()
    rs = conn.execute(select[users.c.is_manager])
    return render_template("private.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
