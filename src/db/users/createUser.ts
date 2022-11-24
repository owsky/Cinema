import { pool } from ".."
import { Role } from "../../models/User"

export default async function createUser(
  email: string,
  fullName: string,
  password: string,
  salt: string,
  role = Role.user
) {
  const client = await pool.connect()
  await client.query(
    "INSERT INTO Users(email, full_name, password, salt, user_role) VALUES($1, $2, $3, $4, $5)",
    [email, fullName, password, salt, role]
  )
  client.release()
}
