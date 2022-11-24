DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
SET search_path to public;
CREATE EXTENSION pg_trgm;

CREATE TYPE user_role_type AS ENUM (
  'user',
  'admin'
);

CREATE TABLE movies (
  movie_id serial PRIMARY KEY,
  title varchar NOT NULL,
  runtime integer NOT NULL,
  year integer NOT NULL,
  plot varchar NOT NULL,
  director varchar NOT NULL,
  genre text NOT NULL,
	actors varchar[] NOT NULL
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
  seat_id serial PRIMARY KEY,
  code integer NOT NULL,
  room varchar NOT NULL,
  CONSTRAINT room_fkey
    FOREIGN KEY (room)
    REFERENCES rooms(room_name)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE projections (
  projection_id serial PRIMARY KEY,
  movie integer,
  room varchar,
  start_date timestamp NOT NULL,
  end_date timestamp NOT NULL,
  price money NOT NULL,
  CONSTRAINT movie_fkey
    FOREIGN KEY (movie)
    REFERENCES movies(movie_id)
		ON UPDATE CASCADE
		ON DELETE SET NULL,
  CONSTRAINT room_fkey
    FOREIGN KEY (room)
    REFERENCES rooms(room_name)
		ON UPDATE CASCADE
		ON DELETE SET NULL
);

CREATE TABLE tickets (
  ticket_id serial PRIMARY KEY,
  user_email varchar,
  projection integer NOT NULL,
  seat integer,
  CONSTRAINT user_email_fkey
    FOREIGN KEY (user_email)
    REFERENCES users(email)
		ON UPDATE CASCADE
		ON DELETE SET NULL,
  CONSTRAINT projection_fkey
    FOREIGN KEY (projection)
    REFERENCES projections(projection_id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
  CONSTRAINT seat_fkey
    FOREIGN KEY (seat)
    REFERENCES seats(seat_id)
		ON UPDATE CASCADE
		ON DELETE SET NULL
);

CREATE FUNCTION check_available_seat()
	RETURNS TRIGGER
	LANGUAGE PLPGSQL
AS
$$
DECLARE
	occupied INTEGER[];
  seatCode INTEGER;
BEGIN
	occupied := ARRAY(SELECT seat FROM tickets WHERE projection = NEW.projection);
	IF NEW.seat = ANY(occupied) THEN
    SELECT code INTO seatCode FROM seats WHERE seat_id = NEW.seat;
		RAISE EXCEPTION 'seat % is already occupied', seatCode;
	END IF;
	RETURN NEW;
END;
$$;
CREATE TRIGGER check_available_seat_trigger
	BEFORE INSERT
	ON "tickets"
	FOR EACH ROW
EXECUTE PROCEDURE check_available_seat();

CREATE FUNCTION check_duplicate_movie()
	RETURNS TRIGGER
	LANGUAGE PLPGSQL
AS
$$
DECLARE
	duplicateTitle text;
	duplicateYear text;
BEGIN
	SELECT title, year INTO duplicateTitle, duplicateYear
	FROM movies
	WHERE title = NEW.title;

	IF FOUND THEN
		IF duplicateTitle = NEW.title AND duplicateYear = NEW.year THEN
			RAISE EXCEPTION 'Movie % is already in the database', NEW.title;
		ELSE
			NEW.title := (NEW.title || ' (' || NEW.year || ')');
		END IF;
	END IF;
	RETURN NEW;
END;
$$;
CREATE TRIGGER check_duplicate_movie_trigger
	BEFORE INSERT
	ON "movies"
	FOR EACH ROW
EXECUTE PROCEDURE check_duplicate_movie();

CREATE FUNCTION check_projection_overlap()
	RETURNS TRIGGER
	LANGUAGE PLPGSQL
AS
$$
DECLARE
	movie_title_overlap varchar;
	start_date_overlap timestamp;
	end_date_overlap timestamp;
BEGIN
	SELECT title, start_date, end_date INTO movie_title_overlap, start_date_overlap, end_date_overlap
	FROM projections JOIN movies ON projections.movie = movies.movie_id
	WHERE
		NEW.room = room AND
		(start_date, end_date) OVERLAPS (NEW.start_date, NEW.end_date);

	IF FOUND THEN
		RAISE EXCEPTION 'New projection overlaps existing projection %: % - %', movie_title_overlap, start_date_overlap, end_date_overlap;
	END IF;

	RETURN NEW;
END;
$$;
CREATE TRIGGER check_projection_overlap_trigger
	BEFORE INSERT
	ON "projections"
	FOR EACH ROW
EXECUTE PROCEDURE check_projection_overlap();