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

-- DIRECTORS
INSERT INTO directors(full_name)
VALUES
  ('Martin Scorsese'),
  ('Christopher Nolan'),
  ('Stanley Kubrick'),
  ('Robert Zemeckis'),
  ('Bong Joon Ho'),
  ('Sam Mendes'),
  ('Christopher Nolan'),
  ('Rod Lurie'),
  ('Dan Scanlon'),
  ('Leigh Whannell'),
  ('Frank Darabont'),
  ('Francis Ford Coppola'),
  ('Peter Jackson'),
  ('Quentin Tarantino'),
  ('Sergio Leone'),
  ('David Yates'),
  ('Jaume Collet-Serra'),
  ('David Gordon Green');

-- MOVIES
INSERT INTO movies
  (title, duration, genre, synopsys, director, release_date)
VALUES
  (
    'Shutter Island',
    139,
    'Thriller',
    'In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.',
    1,
    '2010-02-19'
  ),
  (
    'Inception',
    162,
    'Action',
    'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
    2,
    '2010-07-16'
  ),
  (
    '2001: A Space Odyssey',
    164,
    'Sci-Fi',
    'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.',
    3,
    '1968-04-02'
  ),
  (
    'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb',
    102,
    'Comedy',
    'An insane general triggers a path to nuclear holocaust that a War Room full of politicians and generals frantically tries to stop.',
    3,
    '1964-05-14'
  ),
  (
    'Parasite',
    132,
    'Comedy',
    'With an insightful and searing exploration of human behavior, Parasite is a masterfully crafted film that is a definite must watch.',
    5,
    '2019-11-07'
  ),
  (
    '1917',
    119,
    'Drama',
    '1917 is tense, captivating, meticulous, horrifying and stirring.',
    6,
    '2020-01-23'
  ),
  (
    'Tenet',
    150,
    'Action',
    'The film''s screenplay keeps underlining and explaining its layered plot about technology that can reverse time.',
    7,
    '2020-08-26'
  ),
  (
    'The Outpost',
    123,
    'Action',
    'The Outpost is crafted with precision, expertise and experience. It''s a war drama that transports you to the battlefield in all its cinematic brilliance.',
    8,
    '2020-06-24'
  ),
  (
    'Onward',
    156,
    'Animation',
    'The animation is top-notch and visually appealing. The characters are adequately cartoonish and also highly relatable and humane.',
    9,
    '2020-03-05'
  ),
  (
    'The Invisible Man',
    125,
    'Horror',
    'One of the rare psychological horror-thrillers that should come with a trigger warning, The Invisible Man subverts many genre tropes to keep you looking over your shoulder well after the credits roll.',
    10,
    '2019-03-05'
  ),
  (
    'The Shawshank Redemption',
    142,
    'Drama',
    'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
    11,
    '1994-10-14'
  ),
  (
    'The Godfather',
    175,
    'Drama',
    'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
    12,
    '1972-03-24'
  ),
  (
    'The Dark Knight',
    152,
    'Action',
    'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
    7,
    '2008-07-18'
  ),
  (
    'The Lord of the Rings: The Return of the King',
    201,
    'Adventure',
    'Gandalf and Aragorn lead the World of Men against Sauron''s army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.',
    13,
    '2003-12-17'
  ),
  (
    'Pulp Fiction',
    154,
    'Drama',
    'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
    14,
    '1994-10-14'
  ),
  (
    'The Good, the Bad and the Ugly',
    178,
    'Western',
    'A bounty hunting scam joins two men in an uneasy alliance against a third in a race to find a fortune in gold buried in a remote cemetery.',
    15,
    '1967-12-29'
  );

-- ACTORS
INSERT INTO actors(full_name)
VALUES
  ('Leonardo DiCaprio'),
  ('Keir Dullea'),
  ('Peter Sellers'),
  ('Morgan Freeman'),
  ('Tim Robbins'),
  ('Bob Gunton'),
  ('Marlon Brando'),
  ('Al Pacino'),
  ('James Caan'),
  ('Christian Bale'),
  ('Heath Ledger'),
  ('Aaron Eckhart'),
  ('Elijah Wood'),
  ('Viggo Mortensen'),
  ('Ian McKellen'),
  ('John Travolta'),
  ('Uma Thruman'),
  ('Samuel L. Jackson'),
  ('Clint Eastwood'),
  ('Eli Wallach'),
  ('Lee Van Cleef'),
  ('Emily Mortimer'),
  ('Mark Ruffalo'),
  ('Joseph Gordon-Levitt'),
  ('Ellen Page'),
  ('Gary Lockwood'),
  ('William Sylvester'),
  ('George C. Scott'),
  ('Sterling Hayden'),
  ('Kang-ho Song'),
  ('Sun-kyun Lee'),
  ('Yeo-jeong Jo'),
  ('Dean-Charles Chapman'),
  ('George MacKay'),
  ('Daniel Mays'),
  ('John David Washington'),
  ('Robert Pattinson'),
  ('Elizabeth Debicki'),
  ('Scott Eastwood'),
  ('Caleb Landry Jones'),
  ('Orlando Bloom'),
  ('Tom Holland'),
  ('Chris Pratt'),
  ('Julia Louis-Dreyfus'),
  ('Elisabeth Moss'),
  ('Oliver Jackson-Cohen'),
  ('Harriet Dyer'),
  ('Eddie Redmayne'),
  ('Johnny Depp'),
  ('Katherine Waterston'),
  ('Dwayne Johnson'),
  ('Sarah Shahi'),
  ('Aldis Hodge'),
  ('Jamie Lee Curtis'),
  ('Judy Greer'),
  ('Anthony Michael Hall');

-- CAST
INSERT INTO cast_entry(actor, movie)
VALUES
  (1, 1),
  (2, 1),
  (3, 2),
  (4, 3),
  (11, 4),
  (11, 5),
  (11, 6),
  (12, 7),
  (12, 8),
  (12, 9),
  (13, 10),
  (13, 11),
  (13, 12),
  (14, 13),
  (14, 14),
  (14, 15),
  (15, 16);

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
  ),
  (
    6,
    '2022-05-03 10:00:00',
    '2021-05-03 12:00:00',
    'Room B',
    10.00
  );
