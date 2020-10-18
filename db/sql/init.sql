-- ROOMS
INSERT INTO public.rooms(rooms_name,rooms_capacity) VALUES
    ('Room A', 100),
    ('Room B', 100);

-- SEATS
INSERT INTO public.seats(seats_name, seats_room) VALUES
    ('1A', 1),
    ('2A', 1),
    ('3A', 1),
    ('4A', 1),
    ('5A', 1),
    ('6A', 1),
    ('7A', 1),
    ('8A', 1),
    ('9A', 1),
    ('10A', 1),
    ('1B', 2),
    ('2B', 2),
    ('3B', 2),
    ('4B', 2),
    ('5B', 2),
    ('6B', 2),
    ('7B', 2),
    ('8B', 2),
    ('9B', 2),
    ('10B', 2);

-- DIRECTORS
INSERT INTO public.directors(directors_name) VALUES
    ('Martin Scorsese'),
    ('Christopher Nolan'),
    ('Stanley Kubrick'),
    ('Robert Zemeckis');

-- MOVIES
INSERT INTO public.movies(movies_title, movies_duration, movies_genre, movies_synopsis, movies_director) VALUES
    ('Shutter Island', 139, 'Thriller', 'In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.', 1),
    ('Inception', 162, 'Action', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 2),
    ('2001: A Space Odyssey', 164, 'Sci-Fi', 'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.', 3),
    ('Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 102, 'Comedy', 'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically tries to stop.', 3);

-- ACTORS
INSERT INTO public.actors(actors_fullname) VALUES
    ('Leonardo DiCaprio'),
    ('Keir Dullea'),
    ('Peter Sellers');

-- CAST
INSERT INTO public.cast(cast_movie, cast_actor) VALUES
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3);

-- USERS
INSERT INTO public.users(users_email, users_name, users_surname, users_pwd, users_is_manager) VALUES
    ('jack@aol.com', 'Jack', 'Boeing', 'passwordsicura', False),
    ('jane@hotmail.com', 'Jane', 'Accounting', 'bookkeepingaf', False),
    ('anonymous@gmail.com', 'Anon', 'Chan', 'scriptkiddie', False),
    ('megamanager@gmail.com', 'Kim', 'Schmitz', 'megamanager', True),
    ('manager', 'manager', 'manager', 'manager', True),
    ('user', 'user', 'user', 'user', False);

-- PROJECTIONS
INSERT INTO public.projections(projections_movie, projections_date_time, projections_room, projections_price) VALUES
    (1, '2020-08-01 21:00:00', 1, 10.00),
    (2, '2020-08-01 21:00:00', 2, 10.00),
    (3, '2020-08-02 21:00:00', 1, 10.00),
    (4, '2020-08-02 21:00:00', 2, 10.00);

-- TICKETS
INSERT INTO public.tickets(tickets_user, tickets_projection, tickets_seat) VALUES
    (1, 1, 1),
    (1, 2, 1),
    (2, 1, 2),
    (3, 4, 1);