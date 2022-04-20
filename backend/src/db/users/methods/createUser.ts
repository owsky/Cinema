import { postgres } from "../../.."
import createUserQuery from "../queries/createUserQuery"

export default async function createUser(
  email: string,
  fullName: string,
  password: string,
  salt: string,
  role = "user"
): Promise<void> {
  try {
    const client = await postgres.connect()
    await createUserQuery(client, email, fullName, password, salt, role)
  } catch (e) {
    console.error(e)
    throw e
  }
}
