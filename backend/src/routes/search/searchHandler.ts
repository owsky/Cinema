import postgres from "../../db"

export default async function searchHandler(input: string) {
  const results = await postgres.search(input)
  return results
}
