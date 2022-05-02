import { pool } from ".."
import logger from "../../logger"

export default async function removeFromSchedule(projectionId: number) {
  try {
    await pool.query(
      `
        DELETE FROM projections
        WHERE projection_id = $1
      `,
      [projectionId]
    )
  } catch (e) {
    logger.error(e)
    throw e
  }
}
