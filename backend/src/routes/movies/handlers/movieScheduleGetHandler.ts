import postgres from "../../../db"

export default async function movieScheduleGetHandler(movieId: number) {
  const movie = await postgres.moviesMethods.getMovieSchedule(movieId)
  return movie
}
