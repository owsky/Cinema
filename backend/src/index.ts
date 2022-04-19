import Fastify from "fastify"
import config from "./config"
import routes from "./routes"

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
    }
  })
  fastify.listen(fastify.config.PORT, fastify.config.HOST)
}
start()
