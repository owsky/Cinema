DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
SET search_path to public;

CREATE TYPE movie_genre_type AS ENUM (
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

CREATE TYPE user_role_type AS ENUM (
  'user',
  'admin'
);

CREATE TABLE actors (
  actor_id serial PRIMARY KEY,
  full_name varchar NOT NULL
);

CREATE TABLE directors (
  director_id serial PRIMARY KEY,
  full_name varchar NOT NULL
);

CREATE TABLE movies (
  movie_id serial PRIMARY KEY,
  title varchar NOT NULL,
  duration integer,
  release_date Date,
  synopsys varchar NOT NULL,
  director integer NOT NULL,
  genre movie_genre_type NOT NULL,
  CONSTRAINT director_fkey
    FOREIGN KEY (director)
    REFERENCES directors(director_id)
);

CREATE TABLE cast_entry (
  actor integer,
  movie integer,
  PRIMARY KEY (actor, movie),
  CONSTRAINT actor_fkey
    FOREIGN KEY (actor)
    REFERENCES actors(actor_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
  ,
  CONSTRAINT movie_fkey
    FOREIGN KEY (movie)
    REFERENCES movies(movie_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE users (
  email varchar PRIMARY KEY,
  full_name varchar NOT NULL,
  password varchar NOT NULL,
  salt varchar NOT NULL,
  user_role user_role_type DEFAULT 'user'
);

CREATE TABLE rooms (
  room_name varchar PRIMARY KEY
);

CREATE TABLE seats (
  code integer,
  room varchar NOT NULL,
  PRIMARY KEY (code, room),
  CONSTRAINT room_fkey
    FOREIGN KEY (room)
    REFERENCES rooms(room_name)
);

CREATE TABLE projections (
  projection_id serial PRIMARY KEY,
  movie integer NOT NULL,
  room varchar NOT NULL,
  start_date date NOT NULL,
  end_date date NOT NULL,
  price money NOT NULL,
  CONSTRAINT movie_fkey
    FOREIGN KEY (movie)
    REFERENCES movies(movie_id),
  CONSTRAINT room_fkey
    FOREIGN KEY (room)
    REFERENCES rooms(room_name)
);

CREATE TABLE tickets (
  user_email varchar,
  projection integer,
  PRIMARY KEY (user_email, projection),
  CONSTRAINT user_email_fkey
    FOREIGN KEY (user_email)
    REFERENCES users(email),
  CONSTRAINT projection_fkey
    FOREIGN KEY (projection)
    REFERENCES projections(projection_id)
);
