import { Pool } from "pg"
import logger from "../logger"
import getMoviesMethods from "./movies/moviesMethods"
import getUsersMethods from "./users/usersMethods"

const pool = new Pool({
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

pool.on("error", (err, _client) => {
  logger.error("Unexpected error on idle client", err)
})

const postgres = {
  usersMethods: getUsersMethods(pool),
  moviesMethods: getMoviesMethods(pool),
}
export default postgres
