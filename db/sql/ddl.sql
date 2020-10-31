SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TYPE public.genre AS ENUM ('Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Fantasy', 'Historical',
    'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Western');

CREATE TYPE public.gender AS ENUM ('F', 'M');

CREATE TABLE public.users
(
    users_id         serial PRIMARY KEY,
    users_email      varchar       NOT NULL,
    users_name       varchar       NOT NULL,
    users_gender     public.gender NOT NULL,
    users_surname    varchar       NOT NULL,
    users_pwd        varchar       NOT NULL,
    users_balance    Numeric(12, 2) DEFAULT 0 CHECK ( users_balance >= 0 ),
    users_is_manager boolean       NOT NULL
);

CREATE TABLE public.rooms
(
    rooms_id       serial PRIMARY KEY,
    rooms_name     varchar UNIQUE NOT NULL,
    rooms_capacity int            NOT NULL CHECK ( rooms_capacity > 0 )
);

CREATE TABLE public.directors
(
    directors_id   serial PRIMARY KEY,
    directors_name varchar NOT NULL
);

CREATE TABLE public.movies
(
    movies_id       serial PRIMARY KEY,
    movies_title    varchar                                        NOT NULL,
    movies_duration int CHECK ( movies_duration > 0 ),
    movies_genre    public.genre                                   NOT NULL,
    movies_synopsis varchar                                        NOT NULL,
    movies_date     date,
    movies_director int REFERENCES public.directors (directors_id) NOT NULL
);

CREATE TABLE public.actors
(
    actors_id       serial PRIMARY KEY,
    actors_fullname varchar NOT NULL
);

CREATE TABLE public.projections
(
    projections_id        serial PRIMARY KEY,
    projections_movie     int                                    NOT NULL,
    projections_date_time timestamp without time zone            NOT NULL,
    projections_room      int REFERENCES public.rooms (rooms_id) NOT NULL,
    projections_price     Numeric(12, 2)                         NOT NULL CHECK ( projections_price >= 0 ),
    CONSTRAINT projections_movie_fkey
        FOREIGN KEY (projections_movie)
            REFERENCES public.movies (movies_id)
            ON UPDATE CASCADE
);

CREATE TABLE public.seats
(
    seats_id   serial PRIMARY KEY,
    seats_name varchar UNIQUE NOT NULL,
    seats_room int            NOT NULL,
    CONSTRAINT seats_room_fkey
        FOREIGN KEY (seats_room)
            REFERENCES public.rooms (rooms_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE public.tickets
(
    tickets_id         serial PRIMARY KEY,
    tickets_user       int,
    tickets_projection int NOT NULL,
    tickets_seat       int,
    CONSTRAINT tickets_user_fkey
        FOREIGN KEY (tickets_user)
            REFERENCES public.users (users_id)
            ON UPDATE CASCADE
            ON DELETE SET NULL,
    CONSTRAINT tickets_projection_fkey
        FOREIGN KEY (tickets_projection)
            REFERENCES public.projections (projections_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT tickets_seat_fkey
        FOREIGN KEY (tickets_seat)
            REFERENCES public.seats (seats_id)
            ON UPDATE CASCADE
            ON DELETE SET NULL
);

CREATE TABLE public.cast
(
    cast_id    serial PRIMARY KEY,
    cast_movie int NOT NULL,
    cast_actor int NOT NULL,
    CONSTRAINT cast_movie_fkey
        FOREIGN KEY (cast_movie)
            REFERENCES public.movies (movies_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT cast_actor_fkey
        FOREIGN KEY (cast_actor)
            REFERENCES public.actors (actors_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE VIEW public.sumtickets AS
SELECT COUNT(tickets_id) AS sum_tickets
FROM public.tickets t
         JOIN public.projections p on t.tickets_projection = p.projections_id;

CREATE VIEW public.sumgenres AS
SELECT movies_genre AS genre, COUNT(tickets_id) AS sum_genres
FROM public.tickets
         JOIN public.projections on tickets_projection = projections_id
         JOIN public.movies on projections_movie = movies_id
GROUP BY movies_genre;

CREATE VIEW public.summale AS
SELECT movies_genre AS genre, COUNT(tickets_id) AS summ
FROM public.tickets
         JOIN public.projections ON tickets_projection = projections_id
         JOIN public.movies ON projections_movie = movies_id
         JOIN public.users ON users_id = tickets_user
WHERE users_gender = 'M'
GROUP BY movies_genre;

CREATE VIEW public.rankmovie AS
SELECT movies_id AS id, movies_title AS title, COUNT(tickets_id) AS sold
FROM public.tickets
         JOIN public.projections ON tickets_projection = projections_id
         JOIN public.movies ON projections_movie = movies_id
         JOIN public.users ON users_id = tickets_user
GROUP BY movies_id, movies_title;
