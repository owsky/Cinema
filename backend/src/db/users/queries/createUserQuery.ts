import { PoolClient, QueryResult } from "pg"

export default function createUserQuery(
  client: PoolClient,
  email: string,
  fullName: string,
  password: string,
  salt: string,
  role = "user"
): Promise<QueryResult<any>> {
  return client.query("INSERT INTO Users VALUES ($1, $2, $3, $4, $5)", [
    email,
    fullName,
    password,
    salt,
    role,
  ])
}
