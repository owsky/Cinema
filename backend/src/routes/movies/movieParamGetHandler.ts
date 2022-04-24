import postgres from "../../db"

export default async function getMovie(movieId: number) {
  const movieDeets = await postgres.moviesMethods.getMovie(movieId)
  return movieDeets
}
