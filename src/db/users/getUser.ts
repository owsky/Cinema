import { pool } from ".."
import logger from "../../logger"
import { UserType } from "../../models/User"

export default async function getUser(email: string): Promise<UserType | null> {
  try {
    const client = await pool.connect()
    const { rows } = await client.query("SELECT * FROM Users WHERE email=$1", [
      email,
    ])
    client.release()
    return rows.at(0) as UserType
  } catch (e) {
    logger.error(e)
    return null
  }
}
