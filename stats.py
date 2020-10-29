from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line
from sqlalchemy import text, create_engine

engine = create_engine('postgresql://cinema_user:cinema_password@localhost:5432/cinema_database')


# grafico a linee: può non essere inserita
def get_line() -> Line:
    conn = engine.connect()
    s = text("""SELECT movies_genre AS genre, SUM(CASE WHEN (tickets_id IS NOT NULL) THEN 1 ELSE 0 END) AS sum
                FROM public.tickets
                LEFT JOIN public.projections on tickets_projection = projections_id
                LEFT JOIN public.movies on projections_movie = movies_id GROUP BY movies_genre""")
    datas = conn.execute(s).fetchall()
    conn.close()
    c = (
        Line().add_xaxis([data['genre'] for data in datas]).add_yaxis("Quantity",
                                                                      [data['sum'] for data in datas]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genre"))
    )
    return c


# grafico a barre: seleziona i film in base ai biglietti venduti
def get_bar() -> Bar:
    conn = engine.connect()
    s1 = text("""SELECT movies_id AS id, movies_genre AS genre, SUM(tickets_id) AS summ
                 FROM public.tickets
                 JOIN public.projections ON tickets_projection = projections_id
                 JOIN public.movies ON projections_movie = movies_id
                 JOIN public.users ON users_id = tickets_user 
                 WHERE users_gender='M' GROUP BY movies_id, movies_genre""")

    s2 = text("""SELECT movies_id AS id, movies_genre AS genre, SUM(tickets_id) AS sumf
                 FROM public.tickets
                 JOIN public.projections ON tickets_projection = projections_id
                 JOIN public.movies ON projections_movie = movies_id
                 JOIN public.users ON users_id = tickets_user 
                 WHERE users_gender='F'
                 GROUP BY movies_id, movies_genre""")

    datas1 = conn.execute(s1).fetchall()
    datas2 = conn.execute(s2).fetchall()
    conn.close()
    c = (
        Bar().add_xaxis([data['genre'] for data in datas1]).add_yaxis("Male", [data['summ'] for data in
                                                                               datas1]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genres")).add_yaxis("Female", [data['sumf'] for data in datas2])
    )
    return c


def get_bar2() -> Bar:
    conn = engine.connect()
    s1 = text("""SELECT movies_id AS id, movies_title AS title, SUM(tickets_id) AS sold
                 FROM public.tickets
                 JOIN public.projections ON tickets_projection = projections_id
                 JOIN public.movies ON projections_movie = movies_id
                 JOIN public.users ON users_id = tickets_user 
                 GROUP BY movies_id, movies_title""")

    datas = conn.execute(s1).fetchall()
    print(datas)
    conn.close()
    c = (
        Bar().add_xaxis([data['id'] for data in datas]).add_yaxis("Quantity", [data['sold'] for data in datas]).set_global_opts(title_opts=opts.TitleOpts(title="Movies"))
    )
    return c


# grafico a cerchio: seleziona i generi più preferiti dalle persone
def get_pie() -> Pie:
    conn = engine.connect()
    s = text("SELECT genre, sum_genres*100/sum_tickets AS genre_perc FROM public.sumtickets, public.sumgenres")
    datas = conn.execute(s).fetchall()
    print(datas)
    conn.close()
    c = (
        Pie().add("", [(data['genre'], data['genre_perc']) for data in datas]).set_global_opts(
            title_opts=opts.TitleOpts(title="Genres")).set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )
    return c
