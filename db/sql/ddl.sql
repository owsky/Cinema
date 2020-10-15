SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE public.users (
    users_id serial PRIMARY KEY,
    users_email varchar NOT NULL,
    users_name varchar NOT NULL,
    users_surname varchar NOT NULL,
    users_pwd varchar NOT NULL,
    users_is_manager boolean NOT NULL
);

CREATE TABLE public.rooms (
    rooms_id serial PRIMARY KEY,
    rooms_name varchar UNIQUE NOT NULL,
    rooms_capacity int NOT NULL
);

CREATE TABLE public.directors (
    directors_id serial PRIMARY KEY,
    directors_name varchar NOT NULL
);

CREATE TABLE public.movies (
    movies_id serial PRIMARY KEY,
    movies_title varchar NOT NULL,
    movies_duration int NOT NULL,
    movies_genre varchar NOT NULL,
    movies_synopsis varchar NOT NULL,
    movies_director int REFERENCES public.directors(directors_id) NOT NULL
);

CREATE TABLE public.actors (
    actors_id serial PRIMARY KEY,
    actors_fullname varchar NOT NULL
);

CREATE TABLE public.projections (
    projections_id serial PRIMARY KEY,
    projections_movie int NOT NULL,
    projections_date_time timestamp without time zone NOT NULL,
    projections_room int REFERENCES public.rooms(rooms_id) NOT NULL,
    projections_price Numeric(12,2) NOT NULL,
    CONSTRAINT projections_movie_fkey
        FOREIGN KEY(projections_movie)
        REFERENCES public.movies(movies_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE public.seats (
    seats_id serial PRIMARY KEY,
    seats_name varchar UNIQUE NOT NULL,
    seats_room int NOT NULL,
    CONSTRAINT seats_room_fkey
        FOREIGN KEY(seats_room) 
        REFERENCES public.rooms(rooms_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE public.tickets (
    tickets_id serial PRIMARY KEY,
    tickets_user int NOT NULL,
    tickets_projection int NOT NULL,
    tickets_seat int NOT NULL,
    CONSTRAINT tickets_user_fkey
        FOREIGN KEY(tickets_user)
        REFERENCES public.users(users_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT tickets_projection_fkey
        FOREIGN KEY(tickets_projection)
        REFERENCES public.projections(projections_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT tickets_seat_fkey
        FOREIGN KEY(tickets_seat)
        REFERENCES public.seats(seats_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE public.cast (
    cast_id serial PRIMARY KEY,
    cast_movie int NOT NULL,
    cast_actor int NOT NULL,
    CONSTRAINT cast_movie_fkey
        FOREIGN KEY(cast_movie)
        REFERENCES public.movies(movies_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT cast_actor_fkey
        FOREIGN KEY(cast_actor)
        REFERENCES public.actors(actors_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE VIEW public.projections_info AS
SELECT movies_title, movies_genre, movies_synopsis, movies_director, projections_date_time, projections_room
FROM public.movies, public.projections
WHERE movies_id = projections_movie;