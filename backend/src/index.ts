import Fastify from "fastify"
import { PostgresDb } from "fastify-postgres"
import config from "./config"
import routes from "./routes"

export let postgres: PostgresDb

async function start() {
  const fastify = Fastify({
    logger: true,
  })
  try {
    await config(fastify)
    fastify.register(routes)
  } catch (e) {
    fastify.log.error(e)
  }
  fastify.ready(err => {
    if (err) fastify.log.error(err)
    else {
      postgres = fastify.pg
      fastify.listen(fastify.config.PORT, fastify.config.HOST)
    }
  })
}
start()
