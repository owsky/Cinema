from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from sqlalchemy import text, create_engine

engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')


# returns the most popular genres based on gender
def get_bar() -> Bar:
    conn = engine.connect()

    s1 = text("""SELECT movies_genre AS genre, summ, SUM(tickets_id) AS sumf
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
        Bar().add_xaxis([data['genre'] for data in datas1]).add_yaxis("Female", [data['sumf'] for data in
                                                                                 datas1]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genres")).add_yaxis("Male", [data['summ'] for data in datas1])
    )
    return c


# returns a pie chart of 10 most popular movies
def get_bar2() -> Bar:
    datas = get_popular_movies()
    c = (
        Bar().add_xaxis([data['id'] for data in datas]).add_yaxis("Quantity", [data['sold'] for data in datas])
            .set_global_opts(title_opts=opts.TitleOpts(title="Movies"))

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
    s = text("SELECT genre, sum_genres*100/sum_tickets AS genre_perc FROM public.sumtickets, public.sumgenres")
    datas = conn.execute(s).fetchall()
    conn.close()
    c = (
        Pie().add("", [(data['genre'], data['genre_perc']) for data in datas]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genres")).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )
    return c
