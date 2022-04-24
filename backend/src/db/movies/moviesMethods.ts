import { Pool } from "pg"
import logger from "../../logger"
import { ProjectionType } from "../../models/Projection"

export default function getMoviesMethods(pool: Pool) {
  async function getCurrentSchedule() {
    try {
      const client = await pool.connect()
      const { rows } = await client.query(`
        SELECT 
          projection_id,
          room,
          start_date,
          end_date,
          price,
          title,
          duration,
          release_date,
          synopsys,
          genre,
          full_name as director
        FROM
          projections JOIN movies
            ON projections.movie = movies.movie_id
          JOIN directors
            ON movies.director = directors.director_id
        WHERE projections.start_date > now()
      `)
      return rows as ProjectionType[]
    } catch (e) {
      logger.error(e)
    }
  }

  return {
    getCurrentSchedule,
  }
}
