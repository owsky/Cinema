import { pool } from ".."
import logger from "../../logger"

type MoviesQueryResult = {
  title: string
}

export default async function search(input: string) {
  try {
    const { rows: movieRows } = await pool.query(
      `
      SELECT title
      FROM movies
      WHERE word_similarity(title, $1) > 0.3
    `,
      [input]
    )

    return (movieRows as MoviesQueryResult[]).map(row => row.title)
  } catch (e) {
    logger.error(e)
  }
}
