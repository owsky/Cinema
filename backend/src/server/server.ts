import Fastify, { FastifyInstance } from "fastify"
import logger from "../logger"
import routes from "../routes"
import registerPlugins from "../plugins"

export default async function createServer(): Promise<FastifyInstance> {
  const fastify = Fastify({
    logger: logger,
  })
  await registerPlugins(fastify)
  await fastify.register(routes)
  fastify.ready(err => {
    if (err) throw err
    fastify.swagger()
  })
  return fastify
}
