import { pool } from ".."
import logger from "../../logger"
import { ActorType } from "../../models/Actor"

export default async function getActor(actorId: number) {
  try {
    type QueryResult = {
      actor_id: number
      full_name: string
      starring: string[]
    }
    const { rows } = await pool.query(
      `
      SELECT
        a.actor_id,
        a.full_name,
        array_agg(m.title) as starring
      FROM
        actors a JOIN cast_entry c ON a.actor_id = c.actor
                 JOIN movies m ON m.movie_id = c.movie
      WHERE a.actor_id = $1
      GROUP BY a.actor_id, a.full_name
      `,
      [actorId]
    )
    const typedRows = rows as QueryResult[]
    const results: ActorType = {
      actor_id: typedRows[0].actor_id,
      full_name: typedRows[0].full_name,
      starring: typedRows[0].starring,
    }
    return results
  } catch (e) {
    logger.error(e)
  }
}
