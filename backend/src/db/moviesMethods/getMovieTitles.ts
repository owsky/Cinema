import { pool } from ".."
import logger from "../../logger"

export default async function getMovieTitles(input: string) {
  try {
    type QueryResult = {
      title: string
    }
    const { rows } = await pool.query(
      `
      SELECT title
      FROM movies
      WHERE word_similarity(title, $1) > 0.3
    `,
      [input]
    )
    const typedRows = rows as QueryResult[]
    const titles = typedRows.map(row => {
      return row.title
    })
    return titles
  } catch (e) {
    logger.error(e)
  }
}
