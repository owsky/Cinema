import { pool } from ".."
import logger from "../../logger"
import { MovieType } from "../../models/Movie"

export default async function getAllMovies() {
  try {
    const client = await pool.connect()
    const { rows } = await client.query(`
      SELECT *
      FROM movies
    `)
    return rows as MovieType[]
  } catch (e) {
    logger.error(e)
  }
}
