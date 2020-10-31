

from flask import flash
from flask_login import current_user
from sqlalchemy import text, create_engine
from datetime import datetime
from classes import Projection, User

engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')


# Buy a ticket after checking whether the user has enough money
def purchase(proj_id, selected_seats):
    with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
        with connection.begin():
            s1 = text("SELECT users_balance FROM public.users WHERE users_id = :e1")
            rs1 = connection.execute(s1, e1=current_user.id)
            balance = rs1.fetchone()

            s2 = text("SELECT projections_price FROM public.projections WHERE projections_id = :e2")
            rs2 = connection.execute(s2, e2=proj_id)
            tprice = rs2.fetchone()
            total = balance.users_balance - (tprice.projections_price * len(selected_seats))
            if total < 0:
                connection.close()
            else:
                for x in selected_seats:
                    s = text(
                        "INSERT INTO public.tickets(tickets_user, tickets_projection, tickets_seat) VALUES (:e1, :e2, :e3)")
                    connection.execute(s, e1=current_user.id, e2=proj_id, e3=x)
                s = text("UPDATE public.users SET users_balance = :e1 WHERE users_id = :e2")
                connection.execute(s, e1=total, e2=current_user.id)
                connection.close()
    return


# Given a projection's id it returns a new Projection object with formatted date and time
def format_projections(proj):
    proj_list = list()
    for p in proj:
        proj_date = p.projections_date_time.strftime("%m/%d/%Y")
        proj_hour = p.projections_date_time.strftime("%H:%M:%S")[:5]
        proj_list.append(
            Projection(p.projections_id, proj_date, proj_hour, p.rooms_name, p.projections_price,
                       how_many_seats_left(p[0])))
    return proj_list


# Returns all genres from the enum on the DB
def get_genres():
    conn = engine.connect()
    s = text("SELECT unnest(enum_range(NULL::public.genre)) AS genre")
    rs = conn.execute(s)
    gen = rs.fetchall()
    conn.close()
    return gen


# Returns orders history for a specific user
def get_orders(uid):
    conn = engine.connect()
    s = text("""SELECT movies_title, projections_date_time, rooms_name, seats_name FROM tickets
                JOIN seats ON seats_id=tickets_seat
                JOIN rooms ON rooms_id=seats_room
                JOIN projections ON tickets_projection=projections_id
                JOIN movies ON movies_id=projections_movie
                WHERE tickets_user=:e1
                ORDER BY projections_date_time DESC""")
    rs = conn.execute(s, e1=uid)
    orders = rs.fetchall()
    conn.close()
    return orders


# returns a specific actors (by the given name) or all actors on DB
def get_actor_by_name(name):
    # if name is None then returns all actors
    if not name:
        conn = engine.connect()
        s1 = text("SELECT * FROM actors")
        rs = conn.execute(s1)
        act = rs.fetchall()
    else:
        conn = engine.connect()
        s = text("SELECT * FROM actors WHERE actors_fullname = :n")
        rs = conn.execute(s, n=name)
        act = rs.fetchone()
    conn.close()
    return act


# returns a specific actors (by the given id)
def get_actor_by_id(aid):
    conn = engine.connect()
    s = text("SELECT * FROM public.actors WHERE actors_id = :e")
    rs = conn.execute(s, e=aid)
    act = rs.fetchone()
    conn.close()
    return act


# returns a specific room (by the given name) or all rooms on DB
def get_rooms_by_name(name):
    conn = engine.connect()
    if name:
        s = text("SELECT * FROM rooms WHERE rooms_name = :n")
        rs = conn.execute(s, n=name)
        rid = rs.fetchone()
    # if name is None it returns all rooms
    else:
        s = text("SELECT * FROM rooms")
        rs = conn.execute(s)
        rid = rs.fetchall()
    conn.close()
    return rid


# returns a specific room (by the given id) or all rooms on DB
def get_rooms_by_id(cod):
    conn = engine.connect()
    if cod:
        s = text("SELECT * FROM rooms WHERE rooms_id = :c")
        rs = conn.execute(s, c=cod)
        rid = rs.fetchone()
    # if cod is None it returns all rooms
    else:
        s = text("SELECT * FROM rooms")
        rs = conn.execute(s)
        rid = rs.fetchall()
    conn.close()
    return rid


# Checks for overlaps on a given projection
def check_time(start, end, room):
    conn = engine.connect()
    s = text("""SELECT projections_id FROM public.projections
                JOIN public.movies ON projections_movie=movies_id
                WHERE projections_room = :r AND
                (:st, :e) OVERLAPS (projections_date_time, projections_date_time + (movies_duration * interval '1 minute'))""")
    rs = conn.execute(s, r=room, st=start, e=end)
    ris = rs.fetchone()
    conn.close()
    return ris


# Checks for overlaps on a given projection
def check_time_update(proj, start, end, room):
    conn = engine.connect()
    s = text("""SELECT projections_id FROM public.projections
                JOIN public.movies ON projections_movie=movies_id
                WHERE projections_room = :r AND projections_id <>:p AND
                (:st, :e) OVERLAPS (projections_date_time, projections_date_time + (movies_duration * interval '1 minute'))""")
    rs = conn.execute(s,p=proj, r=room, st=start, e=end)
    ris = rs.fetchone()
    conn.close()
    return ris


# Checks whether exists a relation between an actor and a movie
def check_cast(movid, actid):
    conn = engine.connect()
    s = text("SELECT * FROM public.cast WHERE cast_actor=:a AND cast_movie=:m")
    rs = conn.execute(s, a=actid, m=movid)
    check = rs.fetchone()
    conn.close()
    return check


# returns a specific director (by the given id) or all directors on DB
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


# returns a specific director (by the given name) or all directors on DB
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


def user_by_email(user_email):
    conn = engine.connect()
    s = text("SELECT * FROM public.users WHERE users_email = :e1")
    rs = conn.execute(s, e1=user_email)
    u = rs.fetchone()
    conn.close()
    if u:
        return User(u.users_id, u.users_email, u.users_name, u.users_surname, u.users_pwd, u.users_is_manager,
                    u.users_balance)
    else:
        return None


#  Returns all movies or a specific movie
def get_movies(mov):
    conn = engine.connect()
    # If mov is not None it returns a single movie
    if mov:
        s = text("""SELECT movies_id, movies_title, movies_duration, movies_genre, movies_synopsis, movies_date, directors_name
                    FROM public.movies
                    JOIN public.directors ON movies.movies_director = directors.directors_id
                    WHERE movies_title = :e1""")
        rs = conn.execute(s, e1=mov)
        films = rs.fetchone()
    else:
        s = text("""SELECT movies_id, movies_title, movies_duration, movies_genre, movies_synopsis, movies_date, directors_name
                    FROM movies
                    JOIN directors ON movies_director = directors_id""")
        rs = conn.execute(s)
        films = rs.fetchall()
    conn.close()
    return films


# Returns the movies that are currently being projected
def get_movies_proj():
    conn = engine.connect()
    s = text("""SELECT movies_title, movies_duration, movies_genre, movies_synopsis, movies_date, directors_name
                FROM public.movies
                JOIN directors ON movies_director = directors_id
                WHERE movies_id IN (
                    SELECT movies_id
                    FROM public.movies
                    JOIN public.projections ON movies.movies_id = projections.projections_movie)""")
    rs = conn.execute(s)
    films = rs.fetchall()
    conn.close()
    return films


def get_actors(mov):
    conn = engine.connect()
    if mov:
        s = text("""SELECT * FROM public.movies
                    JOIN public.directors ON movies.movies_director = directors.directors_id
                    JOIN public.cast ON movies_id = public.cast.cast_movie
                    JOIN public.actors ON cast_actor = actors_id
                    WHERE movies_title = :e1""")
        rs = conn.execute(s, e1=mov)
    else:
        s = text("SELECT * FROM actors ORDER BY actors_id")
        rs = conn.execute(s)
    act = rs.fetchall()
    conn.close()
    return act


# returns a specific movie (by the given id)
def get_movie_by_id(id):
    conn = engine.connect()
    s = text("SELECT * FROM movies WHERE movies_id =:cod")
    rs = conn.execute(s, cod=id)
    ris = rs.fetchone()
    conn.close()
    return ris


# returns a specific projection (by the given id)
def get_projection_by_id(id):
    conn = engine.connect()
    s = text("SELECT * FROM projections WHERE projections_id =:cod")
    rs = conn.execute(s, cod=id)
    ris = rs.fetchone()
    conn.close()
    return ris


# returns all future projections (by the given movie's title)
def get_future_projections(title):
    conn = engine.connect()
    s = text("""SELECT * FROM public.projections JOIN public.movies ON projections_movie=movies_id 
                WHERE movies_title=:title AND projections_date_time >=:time""")
    rs = conn.execute(s, title=title, time=str(datetime.now()))
    ris = rs.fetchall()
    conn.close()
    return ris


# returns five movies most recently inserted
def get_last_movies():
    conn = engine.connect()
    s = text("""SELECT movies_title, movies_genre, movies_synopsis, directors_name
                FROM movies JOIN directors ON movies_director = directors_id
                ORDER BY movies_id DESC LIMIT 5""")
    rs = conn.execute(s)
    films = rs.fetchall()
    conn.close()
    return films


def get_projections(mov):
    conn = engine.connect()
    if mov:
        s = text("""SELECT projections_id, projections_date_time, projections_price, movies_title, movies_genre, movies_synopsis, movies_duration, directors_name, rooms_name,
                        (SELECT string_agg(actors_fullname::text, ', ') AS actors
                         FROM public.actors
                         JOIN public.cast ON cast_actor=actors_id
                         JOIN public.movies ON cast_movie=movies_id
                         WHERE movies_title=:e1)
                    FROM public.projections
                    JOIN public.movies ON projections_movie = movies_id
                    JOIN public.directors ON movies_director = directors_id
                    JOIN public.rooms ON projections_room = rooms_id 
                    WHERE movies_title = :e1 AND projections_date_time >= current_date""")
        rs = conn.execute(s, e1=mov)
    else:
        s = text("""SELECT movies_title, projections_date_time, projections_price, projections_id, rooms_name
                    FROM public.projections
                    JOIN public.movies ON projections_movie = movies_id
                    JOIN public.directors ON movies_director = directors_id
                    JOIN public.rooms ON projections_room = rooms_id
                    WHERE projections_date_time >= current_date
                    ORDER BY projections_date_time, movies_title, rooms_name""")
        rs = conn.execute(s)
    proj = rs.fetchall()
    conn.close()
    return proj


# Returns how many seats are not occupied on a specific projection
def how_many_seats_left(proj_id):
    conn = engine.connect()
    s = text("""SELECT rooms_capacity FROM public.rooms
                JOIN public.projections ON rooms.rooms_id = projections.projections_room
                WHERE projections_id = :e1""")
    rs = conn.execute(s, e1=proj_id)
    capacity = rs.fetchone()

    s = text("""SELECT COUNT(tickets_id) as t
                FROM public.tickets
                WHERE tickets_projection = :e1""")
    rs = conn.execute(s, e1=proj_id)
    f = rs.fetchone()
    conn.close()
    return capacity.rooms_capacity - f.t


# Returns the seats that are not occupied on a specific projection
def free_seats(proj_id):
    conn = engine.connect()
    s = text("""SELECT *
                 FROM public.seats
                 JOIN public.rooms On seats.seats_room = rooms.rooms_id
                 JOIN public.projections ON rooms.rooms_id = projections.projections_room
                 WHERE projections_id = :e1 AND
                    seats_id NOT IN (
                        SELECT seats_id
                        FROM public.projections
                        JOIN public.tickets ON tickets_projection = projections_id
                        JOIN public.seats ON tickets_seat = seats_id
                        WHERE projections_id = :e1)""")
    rs = conn.execute(s, e1=proj_id)
    f = rs.fetchall()
    conn.close()
    return f


def get_seat_by_name(room_id, seat_name):
    conn = engine.connect()
    s = text("""SELECT * FROM public.seats JOIN public.rooms ON seats.seats_room = rooms.rooms_id
                WHERE rooms_id = :e1 AND seats_name = :e2 """)
    rs = conn.execute(s, e1=room_id, e2=seat_name)
    se = rs.fetchone()
    conn.close()
    return se


# returns all directors on the DB
def get_directors():
    conn = engine.connect()
    s = text("SELECT * FROM public.directors")
    rs = conn.execute(s)
    dire = rs.fetchall()
    conn.close()
    return dire


# returns all rooms on the DB
def get_rooms():
    conn = engine.connect()
    s = text("SELECT * FROM public.rooms")
    rs = conn.execute(s)
    rooms = rs.fetchall()
    conn.close()
    return rooms


def delete_proj(proj):
    with engine.connect().execution_options(isolation_level="SERIALIZABLE") as conn:
        with conn.begin():
            s = text("""SELECT projections_price, users_id FROM public.tickets
                        JOIN public.users ON tickets.tickets_user = users.users_id
                        JOIN public.projections ON tickets.tickets_projection = projections.projections_id
                        WHERE projections_id = :e1""")
            rs = conn.execute(s, e1=proj)
            refunds = rs.fetchall()
            for r in refunds:
                s = text("""UPDATE public.users SET users_balance = users_balance + :e1 WHERE users_id = :e2""")
                conn.execute(s, e1=r.projections_price, e2=r.users_id)
            s = text("DELETE FROM public.projections WHERE projections_id=:p")
            conn.execute(s, p=proj)
            flash("Projection deleted successfully!")
    conn.close()
    return
