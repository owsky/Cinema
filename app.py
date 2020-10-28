from flask import Flask, render_template, request, redirect, url_for, abort, flash
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, \
    AnonymousUserMixin
from datetime import *
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
                or not request.form['pwd'] or not request.form['gender']:
            flash("Missing information")
        if user_by_email(request.form['email']):
            flash("There's already an account set up to use this email address")
        else:
            conn = engine.connect()
            ins = users.insert()
            conn.execute(ins, [
                {"users_name": request.form['name'], "users_surname": request.form['surname'],
                 "users_email": request.form['email'], "users_gender": request.form['gender'],
                 "users_pwd": request.form['pwd'], "users_is_manager": False}
            ])
            conn.close()
            flash("Signed up successfully")
            return redirect(url_for('home'))
    return render_template("user/signup.html", gen=get_gender())


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
        try:
            purchase(projection, request.form.getlist('seat'))
            flash("Successfully purchased tickets")
        except InsufficientBalanceException as e:
            flash(e.message)
    return render_template("user/purchase.html", seats=free_seats(projection), mov=m.movies_title, proj=projection)


# Manager side
# Update: aggiorna gli attributi di un film (genre, synopsis, director)
@app.route('/edit_movie/<title>', methods=['GET', 'POST'])
@login_required
def edit_movie(title):
    if not current_user.is_manager:
        abort(403)
    m = get_movies(title)
    d = get_directors_by_id(m.movies_director)
    if request.method == 'POST':
        conn = engine.connect()
        director = get_directors_by_name(request.form['director'])
        genre = request.form['genre']
        synopsis = request.form['synopsis']
        s = text("UPDATE movies SET movies_genre=:g, movies_synopsis=:s, "
                 "movies_director=:dr WHERE movies_id =:cod")
        conn.execute(s, g=genre, s=synopsis, dr=director.directors_id, cod=m.movies_id)
        conn.close()
        return render_template('manager/movie_manager.html')
    return render_template('manager/edit_movie.html', movie_to_update=m, direct=d, gen=get_genres(),
                           dir=get_directors_by_name(None), c=get_actors(title))


@app.route('/edit_data', methods=['GET', 'POST'])
@login_required
def edit_data():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        if request.form['edit_obj'] == 'movies':
            return render_template('manager/edit_data.html', mov=get_movies(None))
        elif request.form['edit_obj'] == 'actors':
            return render_template('manager/edit_data.html', act=get_actors(None))
        elif request.form['edit_obj'] == 'directors':
            return render_template('manager/edit_data.html', dir=get_directors())
        else:
            return render_template('manager/edit_data.html', room=get_rooms())
    return render_template('manager/edit_data.html')


def get_directors():
    conn = engine.connect()
    s = text("SELECT * FROM public.directors")
    rs = conn.execute(s)
    dire = rs.fetchall()
    conn.close()
    return dire


def get_rooms():
    conn = engine.connect()
    s = text("SELECT * FROM public.rooms")
    rs = conn.execute(s)
    dire = rs.fetchall()
    conn.close()
    return dire


# (Manager) aggiunge un film
@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        conn = engine.connect()
        title = request.form['title']

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


# (Manager) aggiunge una proiezione controllando che non ci siano interferenze nelle sale
@app.route('/<title>/add_projection', methods=['GET', 'POST'])
@login_required
def add_projection(title):
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        conn = engine.connect()
        mov = get_movies(title)
        room = get_rooms_by_name(request.form['room'])

        if (request.form['date_time']<=datetime.now()):
            flash("Can not add a projection in the past")
        else:
        # inserisce la nuova proiezione
            s1 = text("INSERT INTO public.projections(projections_movie, projections_date_time, projections_room, "
                      "projections_price) VALUES (:m,:t,:r,:p)")
            conn.execute(s1, m=mov.movies_id, t=request.form['date_time'], r=room.rooms_id, p=request.form['price'])

            # seleziona la proiezione che ho appena inserito
            s = text("SELECT projections_id AS mov_proj, movies_id AS mov_id, projections_room AS mov_room, "
                     "projections_date_time AS mov_start, "
                     "projections_date_time + (movies_duration * interval '1 minute') AS mov_end FROM public.projections "
                     "JOIN public.movies ON projections_movie=movies_id WHERE projections_movie=:m AND "
                     "projections_room=:r AND projections_date_time=:t")
            proj_info = (conn.execute(s, m=mov.movies_id, r=room.rooms_id, t=request.form['date_time'])).fetchone()

            # fa un check che non ci siano altri film in proiezione nello stesso orario e nella stessa sala
            if check_time(proj_info.mov_proj, proj_info.mov_start, proj_info.mov_end, proj_info.mov_room) is None and \
                    check_time2(proj_info.mov_proj, proj_info.mov_start, proj_info.mov_end, proj_info.mov_room) is None:
                flash("Projection added successfully")
            else:
                # orario non disponibile, effettua una delete della proiezione appena inserita
                flash("Time not available")
                s2 = text("DELETE FROM projections WHERE projections_id=:p")
                conn.execute(s2, p=proj_info.mov_proj)
        conn.close()
        return render_template('user/movie_info.html', movie=mov,
                               projections=format_projections(get_projections(title)),
                               cast=get_actors(title))
    else:
        return render_template("manager/add_projection.html", m=get_movies(title), room=get_rooms_by_id(None))


# (Manager) aggiunge un regista se non è già presente nel database
@app.route('/add_director', methods=['GET', 'POST'])
@login_required
def add_director():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        #se il regista è già presente ritorna un messaggio
        if get_directors_by_name(request.form['name']) is not None:
            flash("Director has already been added")

        #altrimenti il regista viene inserito nel database
        else:
            conn = engine.connect()
            name = request.form['name']
            s = text("INSERT INTO directors (directors_name) VALUES (:n)")
            conn.execute(s, n=name)
            conn.close()
            return redirect(url_for('add_movie'))
    return render_template("manager/add_director.html")


# (Manager) aggiornamento sul nome del regista
@app.route('/edit_director/<director_id>', methods=['GET', 'POST'])
@login_required
def edit_director(director_id):
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        # se il nome del regista inserito è ridondante ritorna un messaggio
        if get_directors_by_name(request.form['name']) is not None:
            flash("Director already exists")

        # altrimenti procede con l'aggiornamento
        else:
            conn = engine.connect()
            s = text("UPDATE public.directors SET directors_name = :e1 WHERE directors_id = :e2")
            conn.execute(s, e1=request.form['name'], e2=director_id)
            conn.close()
            flash("Done!")
    return render_template('manager/edit_director.html', dir=get_directors_by_id(director_id))


# (Manager) aggiunge una relazione tra un film e un attore
@app.route('/<title>/add_cast', methods=['GET', 'POST'])
@login_required
def add_cast(title):
    if not current_user.is_manager:
        abort(403)
    m = get_movies(title)
    if request.method == 'POST':
        conn = engine.connect()
        a = get_actor_by_name(request.form['actor'])

        # controllo che la relazione tra il film e l'attore non esista già
        if not check_cast(m.movies_id, a.actors_id):
            # procede con l'inserimento nella tabella cast
            addcast = text("INSERT INTO public.cast(cast_movie, cast_actor) VALUES (:m, :a)")
            conn.execute(addcast, m=m.movies_id, a=a.actors_id)
            flash("Actor added successfully!")
        # la relazione è ridondante
        else:
            flash("Actor has already been added!")
        return render_template('user/movie_info.html', movie=m, projections=format_projections(get_projections(title)),
                               cast=get_actors(title))
    return render_template('manager/add_cast.html', movie=m, act=get_actor_by_name(None))


# (Manager) aggiunge un nuovo attore
@app.route('/add_actor', methods=['GET', 'POST'])
@login_required
def add_actor():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        # controlla se il nome dell'attore è ridondante, se sì ritorna un messaggio
        if get_actor_by_name(request.form['actor']) is not None:
            flash("Actor already exists")

        # in caso contrario procede con l'inserimento nel database
        else:
            conn = engine.connect()
            s = text("INSERT INTO public.actors (actors_fullname) VALUES (:n)")
            conn.execute(s, n=request.form['actor'])
            flash("Success")
            conn.close()
    return render_template('manager/add_actor.html')


# (Manager) aggiornamento dell'attore
@app.route('/edit_actor/<actor_id>', methods=['GET', 'POST'])
@login_required
def edit_actor(actor_id):
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        # controlla se il nome dell'attore è ridondante, se sì ritorna un messaggio
        if get_actor_by_name(request.form['name']) is not None:
            flash("Actor already exists")
        # in caso contrario procede con l'aggiornamento nel database
        else:
            conn = engine.connect()
            s = text("""UPDATE public.actors
                        SET actors_fullname = :e1
                        WHERE actors_id = :e2""")
            conn.execute(s, e1=request.form['name'], e2=actor_id)
            conn.close()
            flash("Done!")
    return render_template('manager/edit_actor.html', act=get_actor_by_id(actor_id))


# (Manager) elimina un film dal database
@app.route('/delete_movie/<title>')
@login_required
def delete_movie(title):
    if not current_user.is_manager:
        abort(403)
    conn = engine.connect()
    s = text("SELECT * FROM public.projections JOIN public.movies ON projections.projections_movie = movies.movies_id"
             "WHERE movies_title = :e1")
    rs = conn.execute(s, e1=title)
    if not rs.fetchall():
        s = text("DELETE FROM public.movies WHERE movies_title = :mt")
        conn.execute(s, mt=title)
    else:
        flash("You can't delete movies that have been/are being projected")
    conn.close()
    return redirect(url_for('movies_route'))


# (Manager) elimina una proiezione
@app.route('/<title>/delete_projection/<int:id>')
@login_required
def delete_projection(title, id):
    if not current_user.is_manager:
        abort(403)
    conn = engine.connect()
    # elimina una proiezione
    s = text("DELETE FROM public.projections WHERE projections_id=:p")
    conn.execute(s, p=id)
    flash("Projection deleted successfully!")
    conn.close()
    return render_template('user/movie_info.html', movie=get_movies(title),
                           projections=format_projections(get_projections(title)),
                           cast=get_actors(title))


def get_seat_by_name(room_id, seat_name):
    conn = engine.connect()
    s = text("""SELECT * FROM public.seats JOIN public.rooms ON seats.seats_room = rooms.rooms_id
                WHERE rooms_id = :e1 AND seats_name = :e2 """)
    rs = conn.execute(s, e1=room_id, e2=seat_name)
    se = rs.fetchone()
    conn.close()
    return se


@app.route('/edit_room/<room_id>', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        conn = engine.connect()
        s = text("INSERT INTO public.seats(seats_name, seats_room) VALUES (:e1, :e2)")
        conn.execute(s, e1=request.form['seat_name'], e2=room_id)
        conn.close()
    conn = engine.connect()
    s = text("SELECT * FROM public.seats WHERE seats_room = :e1")
    rs = conn.execute(s, e1=room_id)
    se = rs.fetchall()
    conn.close()
    return render_template('manager/edit_room.html', seats=se, room_id=room_id)


@app.route('/remove_seat/<seat_id>/<room_id>')
@login_required
def remove_seat(seat_id, room_id):
    if not current_user.is_manager:
        abort(403)
    conn = engine.connect()
    s = text("DELETE FROM public.seats WHERE seats_id = :e1")
    conn.execute(s, e1=seat_id)
    conn.close()
    return redirect(url_for('edit_room', room_id=room_id))


@app.route('/add_seat/<room_id>', methods=['GET', 'POST'])
@login_required
def add_seat(room_id):
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        if get_seat_by_name(room_id, request.form['name']) is not None:
            flash("Seat already exists")
        else:
            conn = engine.connect()
            s = text("INSERT INTO public.seats VALUES (:e1, :e2)")
            if request.form['name']:
                li = list(request.form['name'].strip().split(","))
                for n in li:
                    conn.execute(s, e1=n, e2=room_id)
                flash("Success")
    return render_template('manager/add_seat.html', room=room_id)


# (Manager) aggiunge una sala
@app.route('/add_room', methods=['GET', 'POST'])
@login_required
def add_room():
    if not current_user.is_manager:
        abort(403)
    if request.method == 'POST':
        # controlla se il nome della 'room' sia ridondante, se sì ritorna un messaggio
        if get_rooms_by_name(request.form['name']) is not None:
            flash("Room already exists")
        # altrimenti procede con l'inserimento
        else:
            conn = engine.connect()
            s = text ("INSERT INTO public.rooms(rooms_name, rooms_capacity) VALUES (:n, :c)")
            conn.execute(s, n=request.form['name'].strip(), c=request.form['capacity'])
            flash("Success")
            conn.close()
    return render_template('manager/add_room.html')


# selezione degli attori (dal nome)
def get_actor_by_name(name):
    # se non viene specificato il valore name, ritorna tutta la lista 'actors' con tutti i suoi attributi
    if name is None:
        conn = engine.connect()
        s1 = text("SELECT * FROM actors")
        rs = conn.execute(s1)
        act = rs.fetchall()
    # altrimenti ritorna la riga della tabella 'actors' che soddisfa la condizione 'actors_fullname' = name
    else:
        conn = engine.connect()
        s = text("SELECT * FROM actors WHERE actors_fullname = :n")
        rs = conn.execute(s, n=name)
        act = rs.fetchone()
    conn.close()
    return act

# selezione degli attori (dall'id)
def get_actor_by_id(aid):
    #ritorna la riga della tabella actors che soddisfa la condizione 'actors_id' = aid
    conn = engine.connect()
    s = text("SELECT * FROM public.actors WHERE actors_id = :e")
    rs = conn.execute(s, e=aid)
    act = rs.fetchone()
    conn.close()
    return act


# selezione della sala (dal nome)
def get_rooms_by_name(name):
    conn = engine.connect()
    # seleziona la riga della tabella rooms che soddisfa la condizione 'rooms_name' = name
    if name:
        s = text("SELECT * FROM rooms WHERE rooms_name = :n")
        rs = conn.execute(s, n=name)
        rid = rs.fetchone()
    # se non viene specificato il valore name, ritorna tutta la lista 'rooms' con tutti i suoi attributi
    else:
        s = text("SELECT * FROM rooms")
        rs = conn.execute(s)
        rid = rs.fetchall()
    conn.close()
    return rid

# selezione della sala (dall'id)
def get_rooms_by_id(cod):
    conn = engine.connect()
    # seleziona la riga della tabella rooms che soddisfa la condizione 'rooms_id' = cod
    if cod:
        s = text("SELECT * FROM rooms WHERE rooms_id = :c")
        rs = conn.execute(s, c=cod)
        rid = rs.fetchone()
    # se non viene specificato il valore name, ritorna tutta la lista 'rooms' con tutti i suoi attributi
    else:
        s = text("SELECT * FROM rooms")
        rs = conn.execute(s)
        rid = rs.fetchall()
    conn.close()
    return rid

# check per l'inserimento di una proiezione
def check_time2(proj, start, end, room):
    conn = engine.connect()
    # controlla che l'orario 'start' e 'end' non siano in interferenza con altre proiezioni
    # seleziona le interferenze se sono presenti
    s = text(
        "SELECT projections_id FROM public.projections JOIN public.movies ON projections.projections_movie = movies.movies_id"
        "WHERE projections_room =:r AND projections_id<>:p AND projections_date_time >= :s AND "
        "(projections_date_time + (movies_duration * interval '1 minute'))<= :e")
    rs = conn.execute(s, p=proj, r=room, s=start, e=end)
    ris = rs.fetchone()
    conn.close()
    return ris


#check per l'inserimento di una proiezione
def check_time(proj, start, end, room):
    conn = engine.connect()
    # controlla se ci siano altre proiezioni inclusa periodo di tempo tra 'start' e 'end' (= data di inizio e fine della proiezione da inserire)
    # seleziona le interferenze se sono presenti
    s = text("SELECT projections_id FROM public.projections JOIN public.movies ON projections_movie=movies_id WHERE "
             "projections_room = :r AND projections_id <>:p AND (:st BETWEEN projections_date_time AND "
             "projections_date_time + (movies_duration * interval '1 minute') OR :e BETWEEN projections_date_time AND "
             "projections_date_time + (movies_duration * interval '1 minute'))")
    rs = conn.execute(s, p=proj, r=room, st=start, e=end)
    ris = rs.fetchone()
    conn.close()
    return ris


def check_cast(movid, actid):
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
    if mov:
        s = text("""SELECT actors_fullname FROM movies
                    JOIN directors ON movies.movies_director = directors.directors_id
                    JOIN public.cast ON movies_id = public.cast.cast_movie
                    JOIN actors ON cast_actor = actors_id
                    WHERE movies_title = :e1""")
        rs = conn.execute(s, e1=mov)
    else:
        s = text("SELECT * FROM actors ORDER BY actors_id")
        rs = conn.execute(s)
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
        s = text("SELECT * FROM public.projections "
                 "JOIN public.movies ON projections_movie = movies_id "
                 "JOIN public.cast ON movies_id = cast_movie "
                 "JOIN public.actors ON cast_actor = actors_id "
                 "JOIN public.directors ON movies_director = directors_id "
                 "JOIN public.rooms ON projections_room = rooms_id "
                 "WHERE movies_title = :e1 AND projections_date_time >= current_date")
        rs = conn.execute(s, e1=mov)
    else:
        s = text("""SELECT movies_title, projections_date_time, projections_price, rooms_name
                    FROM public.projections
                    JOIN public.movies ON projections_movie = movies_id
                    JOIN public.cast ON movies_id = cast_movie
                    JOIN public.actors ON cast_actor = actors_id
                    JOIN public.directors ON movies_director = directors_id
                    JOIN public.rooms ON projections_room = rooms_id
                    WHERE projections_date_time >= current_date
                    ORDER BY projections_date_time, movies_title, rooms_name""")
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


class InsufficientBalanceException(Exception):
    def __init__(self, balance, message="Insufficient funds"):
        self.balance = balance
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.balance} -> {self.message}'


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
            raise InsufficientBalanceException(balance.users_balance)
        for x in selected_seats:
            s = text(
                "INSERT INTO public.tickets(tickets_user, tickets_projection, tickets_seat) VALUES (:e1, :e2, :e3)")
            connection.execute(s, e1=current_user.id, e2=proj_id, e3=x)
        s = text("UPDATE public.users SET users_balance = :e1 WHERE users_id = :e2")
        connection.execute(s, e1=total, e2=current_user.id)
    return


def format_projections(proj):
    proj_list = list()
    for p in proj:
        date = p.projections_date_time.strftime("%m/%d/%Y")
        hour = p.projections_date_time.strftime("%H:%M:%S")[:5]
        proj_list.append(
            Projection(p.projections_id, date, hour, p.rooms_name, p.projections_price, how_many_seats_left(p[0])))
    return proj_list


# ritorna un array di possibili scelte
def get_gender():
    conn = engine.connect()
    s = text("SELECT unnest(enum_range(NULL::public.gender)) AS gender")
    rs = conn.execute(s)
    gen = rs.fetchall()
    return gen


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
        Line().add_xaxis([data['genre'] for data in datas]).add_yaxis("Quantity",
                                                                      [data['sum'] for data in datas]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genre"))
    )
    return c


# grafico a barre: seleziona i film in base ai biglietti venduti
def get_bar() -> Bar:
    conn = engine.connect()
    s1 = text("SELECT movies_id AS id, movies_genre AS genre, SUM(tickets_id) AS summ FROM "
              "public.tickets JOIN public.projections ON tickets_projection = projections_id JOIN public.movies ON "
              "projections_movie = movies_id JOIN public.users ON users_id = tickets_user "
              "WHERE users_gender='M' GROUP BY movies_id, movies_genre")

    s2 = text("SELECT movies_id AS id, movies_genre AS genre, SUM(tickets_id) AS sumf FROM "
              "public.tickets JOIN public.projections ON tickets_projection = projections_id JOIN public.movies ON "
              "projections_movie = movies_id JOIN public.users ON users_id = tickets_user "
              "WHERE users_gender='F' GROUP BY movies_id, movies_genre")

    datas1 = conn.execute(s1).fetchall()
    datas2 = conn.execute(s2).fetchall()
    conn.close()
    c = (
        Bar().add_xaxis([data['genre'] for data in datas1])
            .add_yaxis("Male", [data['summ'] for data in datas1]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genres"))
            .add_yaxis("Female", [data['sumf'] for data in datas2])
    )
    return c


def pop_movies() -> Bar:
    conn = engine.connect()
    s1 = text("SELECT movies_id AS id, movies_title AS title, SUM(tickets_id) AS sold FROM "
              "public.tickets JOIN public.projections ON tickets_projection = projections_id JOIN public.movies ON "
              "projections_movie = movies_id JOIN public.users ON users_id = tickets_user "
              "GROUP BY movies_id, movies_title")

    datas = conn.execute(s1).fetchall()
    conn.close()
    c = (
        Bar().add_xaxis([data['genre'] for data in datas])
            .add_yaxis("Quantity", [data['sold'] for data in datas]).set_global_opts(
            title_opts=opts.TitleOpts(title="Movies"))
    )
    return c


# grafico a cerchio: seleziona i generi più preferiti dalle persone
def get_pie() -> Pie:
    conn = engine.connect()
    s = text("SELECT genre, sum_genres*100/sum_tickets AS genre_perc FROM public.sumtickets, public.sumgenres")
    datas = conn.execute(s).fetchall()
    print(datas)
    conn.close()
    c = (
        Pie().add("", [(data['genre'], data['genre_perc']) for data in datas]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genres")).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )
    return c


if __name__ == '__main__':
    app.run(debug=True)
