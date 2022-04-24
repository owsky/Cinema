import postgres from "../../db"

export default async function getAllMoviesHandler() {
  const movieDeets = await postgres.moviesMethods.getAllMovies()
  return movieDeets
}
