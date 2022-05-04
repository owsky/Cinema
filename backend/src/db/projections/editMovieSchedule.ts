import { pool } from ".."

interface MovieQuery {
  runtime: number
}

export default async function editMovieSchedule(
  projectionId: number,
  movieId: number,
  startDate: string,
  price: number,
  room: string
) {
  const { rowCount: movieRowCount, rows: movieRows } = await pool.query(
    `
      SELECT runtime
      FROM movies
      WHERE movie_id = $1
    `,
    [movieId]
  )
  if (movieRowCount === 0)
    throw new Error("Movie referred from movie ID parameter doesn't exist")
  const runtime = (movieRows as MovieQuery[])[0].runtime
  const start = new Date(startDate).getTime()
  const endMs = start + runtime * 60 * 1000 + 1
  const fifteenMinutesMs = 1000 * 60 * 15
  const end = new Date(
    Math.ceil(endMs / fifteenMinutesMs) * fifteenMinutesMs
  ).getTime()
  const { rowCount } = await pool.query(
    `
      UPDATE projections
      SET movie = $1, room = $2, start_date = to_timestamp($3), end_date = to_timestamp($4), price = $5
      WHERE projection_id = $6
    `,
    [movieId, room, start / 1000, end / 1000, price, projectionId]
  )
  if (rowCount === 0)
    throw new Error("Trying to update a non-existent projection")
}
