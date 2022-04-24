import postgres from "../../../db"

export default async function getMovieHandler(movieId: number) {
  const movieDeets = await postgres.moviesMethods.getMovie(movieId)
  return movieDeets
}
