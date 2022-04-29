import postgres from "../../../db"

export default async function movieTitleGetHandler(input: string) {
  const results = await postgres.moviesMethods.getMovieTitles(input)
  return results
}
