import { pool } from ".."
import logger from "../../logger"
import { MovieType } from "../../models/Movie"

export default async function getMovie(movieId: number) {
  try {
    const client = await pool.connect()
    const { rows } = await client.query(
      `
      SELECT *
      FROM movies
      WHERE movie_id = $1
    `,
      [movieId]
    )
    logger.info(rows)
    client.release()
    return rows.at(0) as MovieType
  } catch (e) {
    logger.error(e)
  }
}
