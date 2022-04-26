import { pool } from ".."
import logger from "../../logger"
import { PurchaseHistoryType } from "../../models/PurchaseHistory"

export default async function createUser(email: string) {
  try {
    const { rows } = await pool.query(
      `
      SELECT title, start_date, room, seat
      FROM
        tickets t JOIN projections p ON p.projection_id = t.projection
                  JOIN movies m ON p.movie = m.movie_id
      WHERE t.user_email = $1
      ORDER BY start_date DESC, title ASC, seat ASC
    `,
      [email]
    )
    return rows as PurchaseHistoryType[]
  } catch (e) {
    logger.error(e)
  }
}
