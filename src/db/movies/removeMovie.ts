import { pool } from ".."

export default async function removeMovie(movieId: number) {
  const { rowCount } = await pool.query(
    `
    DELETE FROM movies
    WHERE movie_id = $1
  `,
    [movieId]
  )
  if (rowCount === 0) return false
  return true
}
