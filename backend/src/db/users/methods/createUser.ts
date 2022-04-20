import { PostgresDb } from "fastify-postgres"
import createUserQuery from "../queries/createUserQuery"

export default async function createUser(
  db: PostgresDb & Record<string, PostgresDb>,
  email: string,
  fullName: string,
  password: string,
  salt: string,
  role = "user"
): Promise<void> {
  try {
    const client = await db.connect()
    await createUserQuery(client, email, fullName, password, salt, role)
  } catch (e) {
    console.error(e)
    throw e
  }
}
