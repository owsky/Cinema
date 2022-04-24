import { Pool } from "pg"
import logger from "../logger"
import moviesMethods from "./moviesMethods"
import usersMethods from "./users/usersMethods"

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
}
export default postgres
