import { Pool } from "pg"
import logger from "../logger"
import moviesMethods from "./movies"
import usersMethods from "./users"
import search from "./search"
import projectionMethods from "./projections"
import ticketMethods from "./tickets"

export const pool = new Pool({
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

pool.on("error", (err, _client) => {
  logger.error("Unexpected error on idle client", err)
})

const postgres = {
  usersMethods,
  moviesMethods,
  projectionMethods,
  ticketMethods,
  search,
}
export default postgres
