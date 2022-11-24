import { pool } from ".."
import { MovieType } from "../../models/Movie"

export default async function getMovie(movieId: number) {
  const { rows } = await pool.query(
    `
      SELECT *
      FROM movies
      WHERE movie_id = $1
    `,
    [movieId]
  )
  return rows.at(0) as MovieType
}
