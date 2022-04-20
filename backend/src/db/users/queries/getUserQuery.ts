import { PoolClient, QueryResult } from "pg"

export default function getUserQuery(
  client: PoolClient,
  email: string
): Promise<QueryResult<any>> {
  return client.query("SELECT * FROM Users WHERE email=$1", [email])
}
