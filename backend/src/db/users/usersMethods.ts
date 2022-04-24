import { Pool } from "pg"
import logger from "../../logger"
import { UserType } from "../../models/User"

export default function getUsersMethods(pool: Pool) {
  async function getUser(email: string): Promise<UserType | null> {
    try {
      const client = await pool.connect()
      const { rows } = await client.query(
        "SELECT * FROM Users WHERE email=$1",
        [email]
      )
      client.release()
      return rows.at(0) as UserType
    } catch (e) {
      logger.error(e)
      return null
    }
  }

  async function createUser(
    email: string,
    fullName: string,
    password: string,
    salt: string,
    role = "user"
  ) {
    const client = await pool.connect()
    await client.query(
      "INSERT INTO Users(email, full_name, password, salt, user_role) VALUES($1, $2, $3, $4, $5)",
      [email, fullName, password, salt, role]
    )
    client.release()
  }

  return {
    getUser,
    createUser,
  }
}
