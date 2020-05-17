# Requirements

- Install [docker](https://www.docker.com/products/docker-desktop)
- Install [docker compose](https://docs.docker.com/compose/install/)

# How to run

- Open a terminal and run: `docker-compose up`
- Open your favorite browser at `http://localhost:8080`

A PgAdmin page will appear asking for credentials:

- User: `admin@cinema.com`
- Password: `cinema`

Select the `cinema_database` database and type in the following credentials:

- User: `cinema_user`
- Password: `cinema_password`

# How to import edits to init.sql

Open a terminal and run: `docker-compose down -v` and then `docker-compose up --build` again.
*The `-v` option tells docker-compose to delete every Docker volume and mount it again from scratch.*
