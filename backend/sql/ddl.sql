DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
SET search_path to public;
CREATE EXTENSION pg_trgm;

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
  runtime varchar NOT NULL,
  year varchar,
  plot varchar NOT NULL,
  director integer NOT NULL,
  genre text NOT NULL,
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
  seat_id serial PRIMARY KEY,
  code integer NOT NULL,
  room varchar NOT NULL,
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
  ticket_id serial PRIMARY KEY,
  user_email varchar NOT NULL,
  projection integer NOT NULL,
  seat integer NOT NULL,
  CONSTRAINT user_email_fkey
    FOREIGN KEY (user_email)
    REFERENCES users(email),
  CONSTRAINT projection_fkey
    FOREIGN KEY (projection)
    REFERENCES projections(projection_id),
  CONSTRAINT seat_fkey
    FOREIGN KEY (seat)
    REFERENCES seats(seat_id)
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

CREATE FUNCTION add_actors(actor_names text[])
	RETURNS varchar[]
	LANGUAGE PLPGSQL
AS
$$
DECLARE
	actor_name varchar;
	actor_ids integer[];
	actor_id_var integer;
BEGIN
	FOREACH actor_name IN ARRAY actor_names LOOP
		WITH
          inserted as (
            INSERT INTO actors(full_name)
            SELECT (actor_name)
            WHERE NOT EXISTS (
              SELECT actor_id
              FROM actors
              WHERE full_name = actor_name
            )
            RETURNING actor_id
          ),
          selected as (
            SELECT actor_id
            FROM actors
            WHERE full_name = actor_name
          )
		  SELECT actor_id INTO actor_id_var
		  FROM (
			  SELECT actor_id
			  FROM inserted
			  UNION ALL
			  SELECT actor_id
			  FROM selected
		  ) AS foo;
		actor_ids = array_append(actor_ids, actor_id_var);
	END LOOP;
	RETURN actor_ids;
END;
$$;

CREATE FUNCTION add_director(director_name text)
	RETURNS text
	LANGUAGE PLPGSQL
AS
$$
DECLARE
	director_id_var text;
BEGIN
	WITH
	  inserted as (
		INSERT INTO directors(full_name)
		SELECT (director_name)
		WHERE NOT EXISTS (
		  SELECT director_id
		  FROM directors
		  WHERE full_name = director_name
		)
		RETURNING director_id
	  ),
	  selected as (
		SELECT director_id
		FROM directors
		WHERE full_name = director_name
	  )
	  SELECT director_id INTO director_id_var
	  FROM (
		  SELECT director_id
		  FROM inserted
		  UNION ALL
		  SELECT director_id
		  FROM selected
	  ) AS foo;
	  RETURN director_id_var;
END;
$$;