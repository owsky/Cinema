-- ROOMS
INSERT INTO rooms(room_name)
VALUES
  ('Room A'),
  ('Room B');

-- SEATS
INSERT INTO seats(code, room)
VALUES
  (1, 'Room A'),
  (2, 'Room A'),
  (3, 'Room A'),
  (4, 'Room A'),
  (5, 'Room A'),
  (6, 'Room A'),
  (7, 'Room A'),
  (8, 'Room A'),
  (9, 'Room A'),
  (10, 'Room A'),
  (11, 'Room A'),
  (12, 'Room A'),
  (13, 'Room A'),
  (14, 'Room A'),
  (15, 'Room A'),
  (16, 'Room A'),
  (17, 'Room A'),
  (18, 'Room A'),
  (19, 'Room A'),
  (20, 'Room A'),
  (21, 'Room A'),
  (22, 'Room A'),
  (23, 'Room A'),
  (24, 'Room A'),
  (25, 'Room A'),
  (26, 'Room A'),
  (27, 'Room A'),
  (28, 'Room A'),
  (29, 'Room A'),
  (30, 'Room A'),
  (31, 'Room A'),
  (32, 'Room A'),
  (33, 'Room A'),
  (34, 'Room A'),
  (35, 'Room A'),
  (36, 'Room A'),
  (37, 'Room A'),
  (38, 'Room A'),
  (39, 'Room A'),
  (40, 'Room A'),
  (1, 'Room B'),
  (2, 'Room B'),
  (3, 'Room B'),
  (4, 'Room B'),
  (5, 'Room B'),
  (6, 'Room B'),
  (7, 'Room B'),
  (8, 'Room B'),
  (9, 'Room B'),
  (10, 'Room B'),
  (11, 'Room B'),
  (12, 'Room B'),
  (13, 'Room B'),
  (14, 'Room B'),
  (15, 'Room B'),
  (16, 'Room B'),
  (17, 'Room B'),
  (18, 'Room B'),
  (19, 'Room B'),
  (20, 'Room B'),
  (21, 'Room B'),
  (22, 'Room B'),
  (23, 'Room B'),
  (24, 'Room B'),
  (25, 'Room B'),
  (26, 'Room B'),
  (27, 'Room B'),
  (28, 'Room B'),
  (29, 'Room B'),
  (30, 'Room B'),
  (31, 'Room B'),
  (32, 'Room B'),
  (33, 'Room B'),
  (34, 'Room B'),
  (35, 'Room B'),
  (36, 'Room B'),
  (37, 'Room B'),
  (38, 'Room B'),
  (39, 'Room B'),
  (40, 'Room B');

-- MOVIES
INSERT INTO movies
  (title, runtime, genre, year, actors, director, plot)
VALUES
  (
    'Shutter Island',
    139,
    'Thriller',
    2010,
    ARRAY ['Leonardo DiCaprio'],
    'Martin Scorsese',
    'In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.'
  ),
  (
    'Inception',
    162,
    'Action',
    2010,
    ARRAY ['Leonardo DiCaprio'],
    'Christopher Nolan',
    'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.'
  ),
  (
    '2001: A Space Odyssey',
    164,
    'Sci-Fi',
    1968,
    ARRAY ['Keir Dullea'],
    'Stanley Kubrick',
    'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.'
  ),
  (
    'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb',
    102,
    'Comedy',
    1964,
    ARRAY ['Peter Sellers'],
    'Stanley Kubrick',
    'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically tries to stop.'
  ),
  (
    'Parasite',
    132,
    'Comedy',
    2019,
    ARRAY ['Yeo-jeong Cho'],
    'Bong Joon-ho',
    'With an insightful and searing exploration of human behavior, Parasite is a masterfully crafted film that is a definite must watch.'
  );

-- USERS
INSERT INTO users(
  email,
  full_name,
  password,
  salt,
  user_role
  )
VALUES
  --manager's plaintext password: toor
  (
    'manager@mail.com',
    'root',
    '$argon2i$v=19$m=4096,t=3,p=1$c2FsdC4uLi4$WU+a0W6nDM4DLQ1MpH+0lFT3DYChcS8aFHQ3/7JFH78',
    'salt....',
    'admin'
  );

-- PROJECTIONS
INSERT INTO projections(
  movie,
  start_date,
  end_date,
  room,
  price
) VALUES
  (
    1,
    '2022-05-01 21:00:00',
    '2022-05-01 23:30:00',
    'Room A',
    10.00
  ),
  (
    2,
    '2022-05-01 21:00:00',
    '2022-05-01 24:00:00',
    'Room B',
    10.00
  ),
  (
    3,
    '2022-05-02 21:00:00',
    '2022-05-02 24:00:00',
    'Room A',
    10.00
  ),
  (
    4,
    '2022-05-02 21:00:00',
    '2022-05-02 23:00:00',
    'Room B',
    10.00
  ),
  (
    5,
    '2022-05-03 10:00:00',
    '2022-05-03 12:30:00',
    'Room A',
    10.00
  );
