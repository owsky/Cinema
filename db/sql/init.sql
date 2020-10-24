-- ROOMS
INSERT INTO public.rooms(rooms_name,rooms_capacity) VALUES
    ('Room A', 10),
    ('Room B', 10),
    ('Room C', 10),
    ('Room D', 10),
    ('Room E', 10);

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
    ('10B', 2),
    ('1C', 3),
    ('2C', 3),
    ('3C', 3),
    ('4C', 3),
    ('5C', 3),
    ('6C', 3),
    ('7C', 3),
    ('8C', 3),
    ('9C', 3),
    ('10C', 3),
    ('1D', 4),
    ('2D', 4),
    ('3D', 4),
    ('4D', 4),
    ('5D', 4),
    ('6D', 4),
    ('7D', 4),
    ('8D', 4),
    ('9D', 4),
    ('10D', 4),
    ('1E', 5),
    ('2E', 5),
    ('3E', 5),
    ('4E', 5),
    ('5E', 5),
    ('6E', 5),
    ('7E', 5),
    ('8E', 5),
    ('9E', 5),
    ('10E', 5);

-- DIRECTORS
INSERT INTO public.directors(directors_name) VALUES
    ('Martin Scorsese'),
    ('Christopher Nolan'),
    ('Stanley Kubrick'),
    ('Robert Zemeckis'),
    ('Bong Joon Ho'),
    ('Sam Mendes'),
    ('Christopher Nolan'),
    ('Rod Lurie'),
    ('Dan Scanlon'),
    ('Leigh Whannell');



-- MOVIES
INSERT INTO public.movies(movies_title, movies_duration, movies_genre, movies_synopsis, movies_director, movies_date) VALUES
    ('Shutter Island', 139, 'Thriller', 'In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.', 1, '2010-02-19' ),
    ('Inception', 162, 'Action', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 2, '2010-07-16'),
    ('2001: A Space Odyssey', 164, 'Sci-Fi', 'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.', 3, '1968-04-02'),
    ('Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 102, 'Comedy', 'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically tries to stop.', 3, '1964-05-14'),
    ('Parasite',132, 'Comedy', 'With an insightful and searing exploration of human behavior, ‘Parasite’ is a masterfully crafted film that is a definite must watch.', 5, '2019-11-07'),
    ('1917', 119, 'Drama', '‘1917’ is tense, captivating, meticulous, horrifying and stirring.', 6, '2020-01-23'),
    ('Tenet', 150, 'Action', 'The film’s screenplay keeps underlining and explaining its layered plot about technology that can reverse time.', 7, '2020-08-26'),
    ('The Outpost', 123, 'Action', '‘The Outpost’ is crafted with precision, expertise and experience. It’s a war drama that transports you to the battlefield in all its cinematic brilliance.', 8, '2020-06-24'),
    ('Onward', 156, 'Animation', 'The animation is top-notch and visually appealing. The characters are adequately cartoonish and also highly relatable and humane.', 9, '2020-03-05'),
    ('The Invisible Man', 125, 'Horror', 'One of the rare psychological horror-thrillers that should come with a trigger warning, ‘The Invisible Man’ subverts many genre tropes to keep you looking over your shoulder well after the credits roll.', 10, '2019-03-05');



-- ACTORS
INSERT INTO public.actors(actors_fullname) VALUES
    ('Leonardo DiCaprio'),
    ('Keir Dullea'),
    ('Peter Sellers'),
    ('fake actor');

-- CAST
INSERT INTO public.cast(cast_movie, cast_actor) VALUES
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 4),
    (6, 4),
    (7, 4),
    (8, 4),
    (9, 4),
    (10, 4);

-- USERS
INSERT INTO public.users(users_email, users_name, users_surname, users_pwd, users_balance, users_is_manager) VALUES
    ('jack@aol.com', 'Jack', 'Boeing', 'passwordsicura', 100, False),
    ('jane@hotmail.com', 'Jane', 'Accounting', 'bookkeepingaf', 200, False),
    ('anonymous@gmail.com', 'Anon', 'Chan', 'scriptkiddie', 150, False),
    ('megamanager@gmail.com', 'Kim', 'Schmitz', 'megamanager', NULL, True),
    ('manager', 'manager', 'manager', 'manager', NULL, True),
    ('user', 'user', 'user', 'user', 50, False);

-- PROJECTIONS
INSERT INTO public.projections(projections_movie, projections_date_time, projections_room, projections_price) VALUES
    (1, '2020-11-01 21:00:00', 1, 10.00),
    (2, '2020-08-01 21:00:00', 2, 10.00),
    (3, '2020-08-02 21:00:00', 1, 10.00),
    (4, '2020-08-02 21:00:00', 2, 10.00),
    (5, '2020-12-01 10:00:00', 3, 10.00),
    (5, '2021-01-02 10:00:00', 2, 10.00),
    (6, '2021-02-01 11:30:00', 4, 10.00),
    (6, '2021-02-02 11:30:00', 3, 10.00),
    (7, '2021-02-01 15:00:00', 5, 10.00),
    (7, '2021-02-02 15:00:00', 5, 10.00),
    (8, '2021-02-01 15:30:00', 4, 10.00),
    (8, '2021-02-02 15:30:00', 4, 10.00),
    (9, '2021-01-01 20:00:00', 3, 10.00),
    (9, '2021-01-02 20:00:00', 3, 10.00),
    (10, '2021-01-01 19:30:00', 4, 10.00),
    (10, '2021-02-02 19:30:00', 4, 10.00);

-- TICKETS
INSERT INTO public.tickets(tickets_user, tickets_projection, tickets_seat) VALUES
    (1, 1, 1),
    (1, 2, 1),
    (2, 1, 2),
    (3, 4, 1);