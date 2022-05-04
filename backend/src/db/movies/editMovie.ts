import { pool } from ".."
import postgresFormat from "pg-format"
import logger from "../../logger"

export default async function editMovie(
  title: string,
  year: string,
  runtime: string,
  genre: string,
  director: string,
  plot: string,
  actors: string[]
) {
  const client = await pool.connect()
  try {
    await client.query("BEGIN;")
    const { rows: actorsRows } = await client.query(
      postgresFormat(`SELECT add_actors(ARRAY[%L]);`, actors)
    )
    const actorsIds = (actorsRows as { add_actors: number[] }[])[0].add_actors

    const { rows: directorRows } = await client.query(
      `SELECT add_director($1);`,
      [director]
    )
    const directorId = (directorRows as { add_director: number }[])[0]
      .add_director
    const { rows: movieRows } = await client.query(
      `UPDATE movies(title, runtime, year, plot, director, genre)
      VALUES($1, $2, $3, $4, $5, $6)
      WHERE movie_id = $7
      RETURNING movie_id;
      `,
      [title, runtime, year, plot, directorId, genre, movieId]
    )
    logger.info(movieRows)
    const movieId = (movieRows as { movie_id: string }[])[0].movie_id
    await client.query(
      postgresFormat(
        `
        INSERT INTO cast_entry(actor, movie)
        VALUES %L;
      `,
        actorsIds.map(id => [id, movieId])
      )
    )
    await client.query(`COMMIT;`)
  } catch (e) {
    logger.error(e)
    await client.query("ROLLBACK;")
    throw e
  } finally {
    client.release()
  }
}
