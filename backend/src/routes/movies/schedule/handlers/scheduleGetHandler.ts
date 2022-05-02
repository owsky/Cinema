import postgres from "../../../../db"

export default async function scheduleGetHandler(currentWeek?: boolean) {
  return await postgres.moviesMethods.getCurrentSchedule(currentWeek)
}
