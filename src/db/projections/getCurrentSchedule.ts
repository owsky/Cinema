import { endOfWeek, addYears } from "date-fns"
import { pool } from ".."
import logger from "../../logger"
import { ProjectionType } from "../../models/Projection"

export default async function getCurrentSchedule(currentWeek?: boolean) {
  try {
    let cap: Date
    // set cap date to end of current week
    if (currentWeek) cap = endOfWeek(new Date(), { weekStartsOn: 1 })
    // set cap date to next year to include all possible scheduled projections
    else cap = addYears(new Date(), 1)

    const client = await pool.connect()
    const { rows } = await client.query(
      `
      SELECT 
        projection_id,
        room,
        start_date,
        end_date,
        price,
        title,
        runtime,
        year,
        plot,
        genre,
        director,
        actors
      FROM
        projections JOIN movies
          ON projections.movie = movies.movie_id
      WHERE
        projections.start_date >= now() AND
        projections.start_date <= to_timestamp($1)
    `,
      [cap.getTime() / 1000]
    )
    client.release()
    return rows as ProjectionType[]
  } catch (e) {
    logger.error(e)
  }
}
