from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime, Float, Enum

engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')
metadata = MetaData(engine)

actors = Table('actors', metadata,
               Column('actors_id', Integer, primary_key=True),
               Column('actors_fullname', String),
               )
cast = Table('cast', metadata,
             Column('cast_id', Integer, primary_key=True),
             Column('cast_movie', Integer),
             Column('cast_actor', Integer)
             )
directors = Table('directors', metadata,
                  Column('directors_id', Integer, primary_key=True),
                  Column('directors_name', String)
                  )
movies = Table('movies', metadata,
               Column('movies_id', Integer, primary_key=True),
               Column('movies_title', String),
               Column('movies_duration', Integer),
               Column('movies_genre', Enum),
               Column('movies_synopsis', String),
               Column('movies_director', Integer)
               )
rooms = Table('rooms', metadata,
              Column('rooms_id', Integer, primary_key=True),
              Column('rooms_name', String)
              )
seats = Table('seats', metadata,
              Column('seats_id', Integer, primary_key=True),
              Column('seats_name', String),
              Column('seats_room', Integer)
              )
tickets = Table('tickets', metadata,
                Column('tickets_id', Integer, primary_key=True),
                Column('tickets_user', Integer),
                Column('tickets_projection', Integer),
                Column('tickets_seat', Integer)
                )
users = Table('users', metadata,
              Column('users_id', Integer, primary_key=True),
              Column('users_email', String),
              Column('users_name', String),
              Column('users_surname', String),
              Column('users_pwd', String),
              Column('users_is_manager', Boolean)
              )
projections = Table('projections', metadata,
                    Column('projections_id', Integer, primary_key=True),
                    Column('projections_movie', Integer),
                    Column('projections_date_time', DateTime),
                    Column('projections_room', Integer),
                    Column('projections_price', Float),
                    Column('projections_remain', Integer))