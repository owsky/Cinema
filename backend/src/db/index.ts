import { Pool } from "pg"
import logger from "../logger"
import moviesMethods from "./movies"
import usersMethods from "./users"
import search from "./search"
import actorsMethods from "./actors"

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
  actorsMethods,
  search,
}
export default postgres
