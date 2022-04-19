import { PostgresDb } from "fastify-postgres"
import createUserQuery from "../queries/createUserQuery"

export default async function createUser(
  db: PostgresDb & Record<string, PostgresDb>,
  email: string,
  fullName: string,
  password: string
): Promise<void> {
  try {
    const client = await db.connect()
    await client.query(createUserQuery, [email, fullName, password, "user"])
  } catch (e) {
    console.error(e)
    throw e
  }
}
