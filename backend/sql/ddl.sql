SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TYPE public.movie_genre_type AS ENUM (
  'Action',
  'Adventure',
  'Animation',
  'Comedy',
  'Drama',
  'Fantasy',
  'Historical',
  'Horror',
  'Romance',
  'Sci-Fi',
  'Thriller',
  'Western'
);

CREATE TYPE public.user_role_type AS ENUM (
  'user',
  'admin'
);

CREATE TABLE public.actors (
  actor_id serial PRIMARY KEY,
  full_name varchar NOT NULL
);

CREATE TABLE public.movies (
  movie_id serial PRIMARY KEY,
  title varchar NOT NULL,
  synopsys varchar NOT NULL,
  genre public.movie_genre_type NOT NULL
);

CREATE TABLE public.cast (
  actor integer,
  movie integer,
  PRIMARY KEY (actor, movie),
  CONSTRAINT actor_fkey
    FOREIGN KEY (actor)
    REFERENCES public.actors(actor_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
  ,
  CONSTRAINT movie_fkey
    FOREIGN KEY (movie)
    REFERENCES public.movies(movie_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE public.users (
  email varchar PRIMARY KEY,
  full_name varchar NOT NULL,
  password varchar NOT NULL,
  user_role public.user_role_type DEFAULT 'user'
);

CREATE TABLE public.rooms (
  room_id serial PRIMARY KEY,
  name varchar NOT NULL
);

CREATE TABLE public.seats (
  code integer,
  room integer NOT NULL,
  PRIMARY KEY (code, room),
  CONSTRAINT room_fkey
    FOREIGN KEY (room)
    REFERENCES public.rooms(room_id)
);

CREATE TABLE public.projections (
  projection_id serial PRIMARY KEY,
  movie integer NOT NULL,
  room integer NOT NULL,
  start_date date NOT NULL,
  end_date date NOT NULL,
  CONSTRAINT movie_fkey
    FOREIGN KEY (movie)
    REFERENCES public.movies(movie_id),
  CONSTRAINT room_fkey
    FOREIGN KEY (room)
    REFERENCES public.rooms(room_id)
);

CREATE TABLE public.tickets (
  user_email varchar,
  projection integer,
  PRIMARY KEY (user_email, projection),
  CONSTRAINT user_email_fkey
    FOREIGN KEY (user_email)
    REFERENCES public.users(email),
  CONSTRAINT projection_fkey
    FOREIGN KEY (projection)
    REFERENCES public.projections(projection_id)
);
