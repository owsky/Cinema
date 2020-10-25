-- ROOMS
INSERT INTO public.rooms(rooms_id, rooms_name,rooms_capacity) VALUES
    (1, 'Room A', 10),
    (2, 'Room B', 10),
    (3, 'Room C', 10),
    (4, 'Room D', 10),
    (5, 'Room E', 10);

SELECT setval('rooms_rooms_id_seq', (SELECT MAX(rooms_id) from "rooms"));

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
    (20, '10B', 2),
    (21, '1C', 3),
    (22, '2C', 3),
    (23, '3C', 3),
    (24, '4C', 3),
    (25, '5C', 3),
    (26, '6C', 3),
    (27, '7C', 3),
    (28, '8C', 3),
    (29, '9C', 3),
    (30, '10C', 3),
    (31, '1D', 4),
    (32, '2D', 4),
    (33, '3D', 4),
    (34, '4D', 4),
    (35, '5D', 4),
    (36, '6D', 4),
    (37, '7D', 4),
    (38, '8D', 4),
    (39, '9D', 4),
    (40, '10D', 4),
    (41, '1E', 5),
    (42, '2E', 5),
    (43, '3E', 5),
    (44, '4E', 5),
    (45, '5E', 5),
    (46, '6E', 5),
    (47, '7E', 5),
    (48, '8E', 5),
    (49, '9E', 5),
    (50, '10E', 5);

SELECT setval('seats_seats_id_seq', (SELECT MAX(seats_id) from "seats"));

-- DIRECTORS
INSERT INTO public.directors(directors_id, directors_name) VALUES
    (1, 'Martin Scorsese'),
    (2, 'Christopher Nolan'),
    (3, 'Stanley Kubrick'),
    (4, 'Robert Zemeckis'),
    (5, 'Bong Joon Ho'),
    (6, 'Sam Mendes'),
    (7, 'Christopher Nolan'),
    (8, 'Rod Lurie'),
    (9, 'Dan Scanlon'),
    (10, 'Leigh Whannell');

SELECT setval('directors_directors_id_seq', (SELECT MAX(directors_id) from "directors"));

-- MOVIES
INSERT INTO public.movies(movies_id, movies_title, movies_duration, movies_genre, movies_synopsis, movies_director, movies_date) VALUES
    (1, 'Shutter Island', 139, 'Thriller', 'In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.', 1, '2010-02-19' ),
    (2, 'Inception', 162, 'Action', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 2, '2010-07-16'),
    (3, '2001: A Space Odyssey', 164, 'Sci-Fi', 'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.', 3, '1968-04-02'),
    (4, 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 102, 'Comedy', 'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically tries to stop.', 3, '1964-05-14'),
    (5, 'Parasite',132, 'Comedy', 'With an insightful and searing exploration of human behavior, ‘Parasite’ is a masterfully crafted film that is a definite must watch.', 5, '2019-11-07'),
    (6, '1917', 119, 'Drama', '‘1917’ is tense, captivating, meticulous, horrifying and stirring.', 6, '2020-01-23'),
    (7, 'Tenet', 150, 'Action', 'The film’s screenplay keeps underlining and explaining its layered plot about technology that can reverse time.', 7, '2020-08-26'),
    (8, 'The Outpost', 123, 'Action', '‘The Outpost’ is crafted with precision, expertise and experience. It’s a war drama that transports you to the battlefield in all its cinematic brilliance.', 8, '2020-06-24'),
    (9, 'Onward', 156, 'Animation', 'The animation is top-notch and visually appealing. The characters are adequately cartoonish and also highly relatable and humane.', 9, '2020-03-05'),
    (10, 'The Invisible Man', 125, 'Horror', 'One of the rare psychological horror-thrillers that should come with a trigger warning, ‘The Invisible Man’ subverts many genre tropes to keep you looking over your shoulder well after the credits roll.', 10, '2019-03-05');

SELECT setval('movies_movies_id_seq', (SELECT MAX(movies_id) from "movies"));

-- ACTORS
INSERT INTO public.actors(actors_id, actors_fullname) VALUES
    (1, 'Leonardo DiCaprio'),
    (2, 'Keir Dullea'),
    (3, 'Peter Sellers'),
    (4, 'fake actor');

SELECT setval('actors_actors_id_seq', (SELECT MAX(actors_id) from "actors"));

-- CAST
INSERT INTO public.cast(cast_id, cast_movie, cast_actor) VALUES
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 2),
    (4, 4, 3),
    (5, 5, 4),
    (6, 6, 4),
    (7, 7, 4),
    (8, 8, 4),
    (9, 9, 4),
    (10, 10, 4);

SELECT setval('cast_cast_id_seq', (SELECT MAX(cast_id) from "cast"));

-- USERS
INSERT INTO public.users(users_id, users_email, users_name, users_surname, users_pwd, users_balance, users_is_manager) VALUES
    (1, 'jack@aol.com', 'Jack', 'Boeing', 'passwordsicura', 100, False),
    (2, 'jane@hotmail.com', 'Jane', 'Accounting', 'bookkeepingaf', 200, False),
    (3, 'anonymous@gmail.com', 'Anon', 'Chan', 'scriptkiddie', 150, False),
    (4, 'manager', 'manager', 'manager', 'manager', NULL, True),
    (5, 'user', 'user', 'user', 'user', 50, False);

 SELECT setval('users_users_id_seq', (SELECT MAX(users_id) from "users"));

-- PROJECTIONS
INSERT INTO public.projections(projections_id, projections_movie, projections_date_time, projections_room, projections_price) VALUES
    (1, 1, '2020-11-01 21:00:00', 1, 10.00),
    (2, 2, '2020-08-01 21:00:00', 2, 10.00),
    (3, 3, '2020-08-02 21:00:00', 1, 10.00),
    (4, 4, '2020-08-02 21:00:00', 2, 10.00),
    (5, 5, '2020-12-01 10:00:00', 3, 10.00),
    (6, 5, '2021-01-02 10:00:00', 2, 10.00),
    (7, 6, '2021-02-01 11:30:00', 4, 10.00),
    (8, 6, '2021-02-02 11:30:00', 3, 10.00),
    (9, 7, '2021-02-01 15:00:00', 5, 10.00),
    (10, 7, '2021-02-02 15:00:00', 5, 10.00),
    (11, 8, '2021-02-01 15:30:00', 4, 10.00),
    (12, 8, '2021-02-02 15:30:00', 4, 10.00),
    (13, 9, '2021-01-01 20:00:00', 3, 10.00),
    (14, 9, '2021-01-02 20:00:00', 3, 10.00),
    (15, 10, '2021-01-01 19:30:00', 4, 10.00),
    (16, 10, '2021-02-02 19:30:00', 4, 10.00);

SELECT setval('projections_projections_id_seq', (SELECT MAX(projections_id) from "projections"));

-- TICKETS
INSERT INTO public.tickets(tickets_id, tickets_user, tickets_projection, tickets_seat) VALUES
    (1, 1, 1, 1),
    (2, 1, 2, 1),
    (3, 2, 1, 2),
    (4, 3, 4, 1);

SELECT setval('tickets_tickets_id_seq', (SELECT MAX(tickets_id) from "tickets"));