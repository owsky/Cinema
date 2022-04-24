import postgres from "../../db"

export default async function scheduleGetHandler() {
  return await postgres.moviesMethods.getCurrentSchedule()
}
