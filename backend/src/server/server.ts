import Fastify, { FastifyInstance } from "fastify"
import logger from "../logger"
import routes from "../routes"

export default async function createServer(): Promise<FastifyInstance> {
  const fastify = Fastify({
    logger: logger,
  })

  // await setupConfig(fastify)
  await fastify.register(routes)
  return fastify
}
