import { pool } from ".."
import logger from "../../logger"
import { ProjectionType } from "../../models/Projection"

export default async function getMovieSchedule(movieId: number) {
  try {
    const client = await pool.connect()
    const { rows } = await client.query(
      `
      SELECT *
      FROM movies JOIN projections ON movies.movie_id = projections.movie
      WHERE movies.movie_id = $1 AND now() < projections.start_date
    `,
      [movieId]
    )
    client.release()
    return rows as ProjectionType[]
  } catch (e) {
    logger.error(e)
  }
}
