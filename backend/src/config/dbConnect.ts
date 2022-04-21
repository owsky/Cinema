import { Client } from "pg"

export default async function dbConnect() {
  const client = new Client()
  await client.connect()
}
