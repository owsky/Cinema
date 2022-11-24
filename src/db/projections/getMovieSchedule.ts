import { pool } from ".."

import { ProjectionType } from "../../models/Projection"

export default async function getMovieSchedule(movieId: number) {
  const { rows } = await pool.query(
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
      FROM movies JOIN projections ON movies.movie_id = projections.movie
      WHERE movies.movie_id = $1 AND now() < projections.start_date
    `,
    [movieId]
  )

  return rows as ProjectionType[]
}
