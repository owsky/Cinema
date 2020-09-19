-- ROOMS
INSERT INTO public.rooms(rooms_id, rooms_name) VALUES
    (1, 'Room A'),
    (2, 'Room B');

-- SEATS

INSERT INTO public.seats(seats_id, seats_name, seats_room) VALUES
    (1, '1A', 1),
    (2, '2A', 1),
    (3, '3A', 1),
    (4, '4A', 1),
    (5, '5A', 1),
    (6, '6A', 1),
    (7, '7A', 1),
    (8, '8A', 1),
    (9, '9A', 1),
    (10, '10A', 1),
    (11, '1B', 2),
    (12, '2B', 2),
    (13, '3B', 2),
    (14, '4B', 2),
    (15, '5B', 2),
    (16, '6B', 2),
    (17, '7B', 2),
    (18, '8B', 2),
    (19, '9B', 2),
    (20, '10B', 2);

-- MOVIES
INSERT INTO public.movies(movies_id, movies_title, movies_genre, movies_synopsis, movies_director) VALUES
    (1, 'Shutter Island', 'Thriller', 'In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.', 'Martin Scorsese'),
    (2, 'Inception', 'Action', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'Christopher Nolan'),
    ttt(3, '2001: A Space Odyssey', 'Sci-Fi', 'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.', 'Stanley Kubrick'),
    (4, 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 'Comedy', 'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically tries to stop.', 'Stanley Kubrick');

-- ACTORS
INSERT INTO public.actors(actors_id, actors_fullname) VALUES
    (1, 'Leonardo DiCaprio'),
    (2, 'Keir Dullea'),
    (3, 'Peter Sellers');

-- CAST
INSERT INTO public.cast(cast_movie, cast_actor) VALUES
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3);

-- USERS
INSERT INTO public.users(users_id, users_email, users_name, users_surname, users_pwd, users_is_manager) VALUES
    (1, 'jack@aol.com', 'Jack', 'Boeing', 'passwordsicura', False),
    (2, 'jane@hotmail.com', 'Jane', 'Accounting', 'bookkeepingaf', False),
    (3, 'anonymous@gmail.com', 'Anon', 'Chan', 'imgoodlulz', False),
    (4, 'megamanager@gmail.com', 'Kim', 'Schmitz', 'fuckfbi', True),
    (5, 'test', 'test', 'test', 'test', True);

-- PROJECTIONS
INSERT INTO public.projections(projections_id, projections_movie, projections_date_time, projections_room) VALUES
    (1, 1, '2020-08-01 21:00:00', 1),
    (2, 2, '2020-08-01 21:00:00', 2),
    (3, 3, '2020-08-02 21:00:00', 1),
    (4, 4, '2020-08-02 21:00:00', 2);

-- TICKETS
INSERT INTO public.tickets(tickets_id, tickets_user, tickets_projection, tickets_seat) VALUES
    (1, 1, 1, 1),
    (2, 1, 2, 1),
    (3, 2, 1, 2),
    (4, 3, 4, 1);