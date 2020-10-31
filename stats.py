from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from sqlalchemy import text, create_engine

engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')


# returns the most popular genres based on gender
def get_bar() -> Bar:
    conn = engine.connect()

    s1 = text("""SELECT movies_genre AS genre, summ, COUNT(tickets_id) AS sumf
                 FROM public.tickets
                 JOIN public.projections ON tickets_projection = projections_id
                 JOIN public.movies ON projections_movie = movies_id
                 JOIN public.users ON users_id = tickets_user
                 JOIN public.summale ON genre = movies_genre
                 WHERE users_gender='F'
                 GROUP BY movies_genre, summ""")

    datas1 = conn.execute(s1).fetchall()
    conn.close()
    c = (
        Bar().add_xaxis([data['genre'] for data in datas1])
             .add_yaxis("Female", [data['sumf'] for data in datas1])
             .add_yaxis("Male", [data['summ'] for data in datas1])
    )
    return c


# function that returns 10 most popular movies
def get_popular_movies():
    conn = engine.connect()
    s = text("""SELECT *
                 FROM public.rankmovie 
                 ORDER BY sold DESC LIMIT 10""")
    rs = conn.execute(s)
    ris = rs.fetchall()
    conn.close()
    return ris


# returns a pie chart of genres' popularity in percentage
def get_pie() -> Pie:
    conn = engine.connect()
    s = text("""SELECT movies_genre AS genre, COUNT(tickets_id) AS sum_genres
                FROM public.tickets
                JOIN public.projections on tickets_projection = projections_id
                JOIN public.movies on projections_movie = movies_id
                GROUP BY movies_genre""")
    datas = conn.execute(s).fetchall()
    conn.close()
    c = (
        Pie().add("", [(data['genre'], data['sum_genres']) for data in datas])
             .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    return c
