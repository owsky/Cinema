import secrets
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import text, create_engine

from classes import User, Anonymous, InsufficientBalanceException, TimeNotAvailableException, man_required
from functions import get_last_movies, user_by_email, get_orders, get_projections, get_movies, get_actors, \
    format_projections, purchase, free_seats, get_genres, get_directors_by_name, get_directors_by_id, get_directors, \
    get_rooms, get_rooms_by_name, check_time, check_time2, get_rooms_by_id, get_actor_by_name, get_actor_by_id, \
    get_seat_by_name, delete_proj, get_movies_proj
from stats import get_bar, get_pie

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous


# Loads the users from the DB and creates a respective object
@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    s = text("SELECT * FROM public.users WHERE users_id = :e1")
    rs = conn.execute(s, e1=user_id)
    u = rs.fetchone()
    conn.close()
    return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd, u.users_is_manager, u.users_balance)


@app.route('/')
def home():
    return render_template("user/index.html", films=get_last_movies())


# Creates a new user entry in the DB if the provided email is not already in use
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if user_by_email(request.form['email']):
            flash("There's already an account set up to use this email address")
        else:
            conn = engine.connect()
            s = text("""INSERT INTO public.users(users_name, users_surname, users_email, users_pwd, users_gender, users_is_manager)
                        VALUES (:e1, :e2, :e3, :e4, :e5, False)""")
            conn.execute(s, e1=request.form['name'], e2=request.form['surname'], e3=request.form['email'],
                         e4=request.form['pwd'], e5=request.form['gender'])
            conn.close()
            flash("Signed up successfully")
            return redirect(url_for('home'))
    return render_template("user/signup.html")


# Logs the user in if there's a match in the DB
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        s = text("SELECT * FROM public.users WHERE users_email = :e1")
        rs = conn.execute(s, e1=request.form['user'])
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


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Renders the user profile page with all the order history
@app.route('/profile')
@login_required
def profile():
    return render_template("user/profile.html", info=get_orders(current_user.id))


# Lets the user change their profile information
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        conn = engine.connect()
        s = text("""UPDATE public.users SET users_name = :e1, users_surname = :e2, users_email = :e3
                    WHERE users_id = :e4""")
        conn.execute(s, e1=request.form['name'], e2=request.form['surname'], e3=request.form['email'],
                     e4=current_user.id)
        conn.close()
        current_user.name = request.form['name']
        current_user.surname = request.form['surname']
        current_user.email = request.form['email']
        return redirect(url_for('profile'))
    return render_template('user/edit_profile.html')


# Deletes a user from the DB while preserving order history
@app.route('/delete_profile', methods=['GET', 'POST'])
@login_required
def delete_profile():
    conn = engine.connect()
    s = text("DELETE FROM public.users WHERE users_id = :e")
    uid = current_user.id
    logout_user()
    conn.execute(s, e=uid)
    conn.close()
    flash("Successfully deleted user data")
    return redirect(url_for('home'))


# Renders the movies page with all the movies that are currently being projected
@app.route('/movies', methods=['GET', 'POST'])
def movies_list():
    # If the page gets loaded with a POST request it applies the filter provided by the user through the GUI
    if request.method == 'POST':
        conn = engine.connect()
        if request.form['filter_select'] == 'genre':
            s = text("""SELECT * FROM public.movies
                        JOIN public.directors ON movies_director = directors_id
                        WHERE movies_genre = :e1""")
            rs = conn.execute(s, e1=request.form['genre'])
            return render_template('movies.html', movies=rs, gen=get_genres(), dir=get_directors(), act=get_actors(None))
        elif request.form['filter_select'] == 'director':
            s = text("""SELECT * FROM public.movies
                        JOIN public.directors ON movies_director = directors_id
                        WHERE directors_name = :e1""")
            rs = conn.execute(s, e1=request.form['director'])
            return render_template('movies.html', movies=rs, gen=get_genres(), dir=get_directors(), act=get_actors(None))
        else:
            s = text("""SELECT * FROM public.movies
                        JOIN public.directors ON movies_director = directors_id
                        WHERE movies_id IN (
                            SELECT movies_id FROM public.movies
                            JOIN public.cast ON movies_id = cast_movie
                            JOIN public.actors ON cast_actor = actors_id
                            JOIN public.projections ON movies.movies_id = projections.projections_movie
                            WHERE actors_fullname = :e1)""")
            rs = conn.execute(s, e1=request.form['actor'])
            return render_template('movies.html', movies=rs, gen=get_genres(), dir=get_directors(), act=get_actors(None))
    return render_template("movies.html", movies=get_movies_proj(), gen=get_genres(), dir=get_directors(), act=get_actors(None))


# Shows the list of coming soon movies
@app.route('/coming_soon')
def coming_soon():
    conn = engine.connect()
    s = text("""SELECT movies_title, movies_duration, movies_genre, movies_synopsis, movies_date
                FROM public.movies
                JOIN public.directors ON movies.movies_director = directors.directors_id
                WHERE movies_id NOT IN (
                    SELECT movies_id FROM public.movies
                    JOIN public.projections ON movies.movies_id = projections.projections_movie)
                AND movies_date > current_date""")
    c = conn.execute(s).fetchall()
    conn.close()
    return render_template('user/coming_soon.html', mov=c)


# Dinamically renders a movie page upon request with the provided movie title
@app.route('/<title>')
def movie_info(title):
    m = get_movies(title)
    if not m:
        abort(404)
    proj = get_projections(title)
    try:
        return render_template("user/movie_info.html", movie=m, projections=format_projections(proj),
                               cast=get_actors(title))
    except TimeNotAvailableException as e:
        flash(e.message)


# Renders the purchase page where the user can buy tickets for a specific projection
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


# Renders a hub where a manager can add new or edit existing information on the database
@app.route('/edit_data', methods=['GET', 'POST'])
@login_required
@man_required
def edit_data():
    if request.method == 'POST':
        if request.form['edit_obj'] == 'movies':
            return render_template('manager/edit_data.html', mov=get_movies(None))
        elif request.form['edit_obj'] == 'actors':
            return render_template('manager/edit_data.html', act=get_actors(None))
        elif request.form['edit_obj'] == 'directors':
            return render_template('manager/edit_data.html', dir=get_directors())
        elif request.form['edit_obj'] == 'projections':
            return render_template('manager/edit_data.html', proj=get_projections(None))
        elif request.form['edit_obj'] == 'rooms':
            return render_template('manager/edit_data.html', room=get_rooms())
        else:
            return render_template('manager/edit_data.html')
    return render_template('manager/edit_data.html')


# Lets a manager edit movies information
@app.route('/edit_movie/<title>', methods=['GET', 'POST'])
@login_required
@man_required
def edit_movie(title):
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


# Lets a manager add a new movie on the DB
@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
@man_required
def add_movie():
    if request.method == 'POST':
        conn = engine.connect()
        title = request.form['title']
        genre = request.form['genre']
        duration = request.form['duration']
        synopsis = request.form['synopsis']
        rel_date = request.form['day']
        director = get_directors_by_name(request.form['director'])

        if get_movies(request.form['title']):
            flash("Movie's name already exists, add at the end it's release date in brackets")

        s = text("INSERT INTO movies (movies_title, movies_genre, movies_duration, movies_synopsis, movies_date, "
                 "movies_director) VALUES (:t, :g, :d, :s, :dt, :dr)")
        conn.execute(s, t=title, g=genre, d=duration, s=synopsis, dt=rel_date, dr=director.directors_id)
        conn.close()
        flash("Movie added successfully!")
        return redirect(url_for('movies_list'))
    return render_template("manager/add_movie.html", gen=get_genres(), dir=get_directors_by_name(None))


# Lets a manager add a new projections on the schedule from the movie info page
@app.route('/<title>/add_projection', methods=['GET', 'POST'])
@login_required
@man_required
def add_projection_movie(title):
    if request.method == 'POST':
        mov = get_movies(title)
        room = get_rooms_by_name(request.form['room'])

        if request.form['date_time'] <= datetime.now():
            flash("Can not add a projection in the past")
        else:
            with engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
                with conn.begin():
                    s1 = text(
                        "INSERT INTO public.projections(projections_movie, projections_date_time, projections_room, "
                        "projections_price) VALUES (:m,:t,:r,:p)")
                    conn.execute(s1, m=mov.movies_id, t=request.form['date_time'], r=room.rooms_id,
                                 p=request.form['price'])

                    # Queries the DB for the just added projection
                    s = text("SELECT projections_id AS mov_proj, movies_id AS mov_id, projections_room AS mov_room, "
                             "projections_date_time AS mov_start, "
                             "projections_date_time + (movies_duration * interval '1 minute') AS mov_end FROM public.projections "
                             "JOIN public.movies ON projections_movie=movies_id WHERE projections_movie=:m AND "
                             "projections_room=:r AND projections_date_time=:t")
                    proj_info = (
                        conn.execute(s, m=mov.movies_id, r=room.rooms_id, t=request.form['date_time'])).fetchone()
                    # Checks if the projection's timestamp overlaps with preexisting projections on the schedule
                    if not check_time(proj_info.mov_proj, proj_info.mov_start, proj_info.mov_end,
                                      proj_info.mov_room) and \
                            not check_time2(proj_info.mov_proj, proj_info.mov_start, proj_info.mov_end,
                                            proj_info.mov_room):
                        flash("Projection added successfully")
                    else:
                        raise TimeNotAvailableException(proj_info.mov_start)
            conn.close()
        return render_template('user/movie_info.html', movie=mov,
                               projections=format_projections(get_projections(title)),
                               cast=get_actors(title))
    else:
        return render_template("manager/add_projection.html", m=get_movies(title), room=get_rooms_by_id(None))


# Lets a manager add a new director
@app.route('/add_director', methods=['GET', 'POST'])
@login_required
@man_required
def add_director():
    if request.method == 'POST':
        if get_directors_by_name(request.form['name']):
            flash("Director has already been added")

        else:
            conn = engine.connect()
            name = request.form['name']
            s = text("INSERT INTO directors (directors_name) VALUES (:n)")
            conn.execute(s, n=name)
            conn.close()
            return redirect(url_for('add_movie'))
    return render_template("manager/add_director.html")


# Lets a manager edit a director's information
@app.route('/edit_director/<director_id>', methods=['GET', 'POST'])
@login_required
@man_required
def edit_director(director_id):
    if request.method == 'POST':
        if get_directors_by_name(request.form['name']):
            flash("Director already exists")
        else:
            conn = engine.connect()
            s = text("UPDATE public.directors SET directors_name = :e1 WHERE directors_id = :e2")
            conn.execute(s, e1=request.form['name'], e2=director_id)
            conn.close()
            flash("Done!")
    return render_template('manager/edit_director.html', dir=get_directors_by_id(director_id))


# Lets a manager add an actor to a movie's cast
@app.route('/<title>/add_cast', methods=['GET', 'POST'])
@login_required
@man_required
def add_cast(title):
    m = get_movies(title)
    if request.method == 'POST':
        conn = engine.connect()
        a = get_actor_by_name(request.form['actor'])

        addcast = text("""INSERT INTO public.cast(cast_movie, cast_actor) VALUES (:m, :a)
                          ON CONFLICT DO NOTHING""")
        conn.execute(addcast, m=m.movies_id, a=a.actors_id)
        flash("Actor added successfully!")
        return render_template('user/movie_info.html', movie=m, projections=format_projections(get_projections(title)),
                               cast=get_actors(title))
    return render_template('manager/add_cast.html', movie=m, act=get_actor_by_name(None))


# Lets a manager add a new actor on the DB
@app.route('/add_actor', methods=['GET', 'POST'])
@login_required
@man_required
def add_actor():
    if request.method == 'POST':
        # Checks whether the actor tuple already exists
        if get_actor_by_name(request.form['actor']):
            flash("Actor already exists")
        else:
            conn = engine.connect()
            s = text("INSERT INTO public.actors (actors_fullname) VALUES (:n)")
            conn.execute(s, n=request.form['actor'])
            flash("Success")
            conn.close()
    return render_template('manager/add_actor.html')


# Lets a manager edit an actor's information
@app.route('/edit_actor/<actor_id>', methods=['GET', 'POST'])
@login_required
@man_required
def edit_actor(actor_id):
    if request.method == 'POST':
        # Checks whether the actor's new name already exists on the DB
        if get_actor_by_name(request.form['name']):
            flash("Actor already exists")
        else:
            conn = engine.connect()
            s = text("""UPDATE public.actors
                        SET actors_fullname = :e1
                        WHERE actors_id = :e2""")
            conn.execute(s, e1=request.form['name'], e2=actor_id)
            conn.close()
            flash("Done!")
    return render_template('manager/edit_actor.html', act=get_actor_by_id(actor_id))


# Lets a manager delete a movie from the DB if it doesn't have any associated projection
@app.route('/delete_movie/<title>')
@login_required
@man_required
def delete_movie(title):
    conn = engine.connect()
    s = text("""SELECT * FROM public.projections JOIN public.movies ON projections.projections_movie = movies.movies_id
                WHERE movies_title = :e1""")
    rs = conn.execute(s, e1=title)
    if not rs.fetchall():
        s = text("DELETE FROM public.movies WHERE movies_title = :mt")
        conn.execute(s, mt=title)
    else:
        flash("You can't delete movies that have been/are being projected")
    conn.close()
    return redirect(url_for('movies_list'))


# Lets a manager delete a projection and refunds sold tickets from the edit data page
@app.route('/delete<proj_id>')
@login_required
@man_required
def delete_projection(proj_id):
    delete_proj(proj_id)
    return redirect(url_for('edit_data'))


# Lets a manager delete a projection and refunds sold tickets from the movie info page
@app.route('/delete/<title>/<proj>')
@login_required
@man_required
def delete_projection_movie(title, proj):
    delete_proj(proj)
    return redirect(url_for('movie_info', title=title))


# Lets a manager edit a room's information
@app.route('/edit_room/<room_id>', methods=['GET', 'POST'])
@login_required
@man_required
def edit_room(room_id):
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


# Lets a manager delete seats from a room
@app.route('/remove_seat/<seat_id>/<room_id>')
@login_required
@man_required
def remove_seat(seat_id, room_id):
    conn = engine.connect()
    s = text("DELETE FROM public.seats WHERE seats_id = :e1")
    conn.execute(s, e1=seat_id)
    conn.close()
    return redirect(url_for('edit_room', room_id=room_id))


# Lets a manager add a seat to a room
@app.route('/add_seat/<room_id>', methods=['GET', 'POST'])
@login_required
@man_required
def add_seat(room_id):
    if request.method == 'POST':
        if get_seat_by_name(room_id, request.form['name']):
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


# Lets a manager add a new room
@app.route('/add_room', methods=['GET', 'POST'])
@login_required
@man_required
def add_room():
    if request.method == 'POST':
        # controlla se il nome della 'room' sia ridondante, se sì ritorna un messaggio
        if get_rooms_by_name(request.form['name']):
            flash("Room already exists")
        # altrimenti procede con l'inserimento
        else:
            conn = engine.connect()
            s = text("INSERT INTO public.rooms(rooms_name, rooms_capacity) VALUES (:n, :c)")
            conn.execute(s, n=request.form['name'].strip(), c=request.form['capacity'])
            flash("Success")
            conn.close()
    return render_template('manager/add_room.html')


# Shows statistics generated from user data
@app.route('/show_echarts')
@login_required
@man_required
def show_echarts():
    bar = get_bar()
    pie = get_pie()
    return render_template("manager/show_echarts.html", bar_options=bar.dump_options(), pie_options=pie.dump_options())


if __name__ == '__main__':
    app.run(debug=True)
