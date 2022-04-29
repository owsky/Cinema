import { pool } from ".."
import logger from "../../logger"

type MoviesQueryResult = {
  title: string
}

type PersonsQueryResult = {
  full_name: string
}

export default async function search(input: string) {
  try {
    const moviesSearchPromise = pool.query(
      `
      SELECT title
      FROM movies
      WHERE word_similarity(title, $1) > 0.3
    `,
      [input]
    )

    const actorsSearchPromise = pool.query(
      `
      SELECT full_name
      FROM actors
      WHERE word_similarity(full_name, $1) > 0.2
      UNION ALL
      SELECT full_name
      FROM directors
      WHERE word_similarity(full_name, $1) > 0.2
    `,
      [input]
    )

    const queriesResults = await Promise.all([
      moviesSearchPromise,
      actorsSearchPromise,
    ])

    logger.info(queriesResults[1])

    const movies = queriesResults[0].rows as MoviesQueryResult[]
    const actors = queriesResults[1].rows as PersonsQueryResult[]
    const results = movies
      .map(row => row.title)
      .concat(actors.map(row => row.full_name))
    return results
  } catch (e) {
    logger.error(e)
  }
}
