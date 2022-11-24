import { pool } from ".."

interface MovieQuery {
  runtime: number
}

export default async function addToSchedule(
  movieId: number,
  startDate: string,
  price: number,
  room: string
) {
  const { rows: movieRows } = await pool.query(
    `
    SELECT runtime
    FROM movies
    WHERE movie_id = $1
  `,
    [movieId]
  )
  const runtime = (movieRows as MovieQuery[])[0].runtime
  const start = new Date(startDate).getTime()
  const endMs = start + runtime * 60 * 1000 + 1
  const fifteenMinutesMs = 1000 * 60 * 15
  const end = new Date(
    Math.ceil(endMs / fifteenMinutesMs) * fifteenMinutesMs
  ).getTime()
  await pool.query(
    `
    INSERT INTO projections(movie, room, start_date, end_date, price)
    VALUES ($1, $2, to_timestamp($3), to_timestamp($4), $5)
  `,
    [movieId, room, start / 1000, end / 1000, price]
  )
}
