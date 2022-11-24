import { pool } from ".."

interface MovieQuery {
  movie_id: number
  title: string
  runtime: number
  year: number
  plot: string
  genre: string
  actors: string[]
  director: string
}

export default async function editMovie(
  movieId: number,
  title?: string,
  year?: string,
  runtime?: string,
  genre?: string,
  director?: string,
  plot?: string,
  actors?: string[]
) {
  const { rows: movieRows } = await pool.query(
    `SELECT * FROM movies WHERE movie_id = $1`,
    [movieId]
  )
  const movieTuple = (movieRows as MovieQuery[])[0]
  const movieTitle = title ? title : movieTuple.title
  const movieYear = year ? year : movieTuple.year
  const movieRuntime = runtime ? runtime : movieTuple.runtime
  const movieGenre = genre ? genre : movieTuple.genre
  const movieDirector = director ? director : movieTuple.director
  const moviePlot = plot ? plot : movieTuple.plot
  const movieActors = actors ? actors : movieTuple.actors
  await pool.query(
    `
    UPDATE movies
    SET title = $2, year = $3, runtime = $4, genre = $5, director = $6, plot = $7, actors = $8
    WHERE movie_id = $1
  `,
    [
      movieId,
      movieTitle,
      movieYear,
      movieRuntime,
      movieGenre,
      movieDirector,
      moviePlot,
      movieActors,
    ]
  )
}
