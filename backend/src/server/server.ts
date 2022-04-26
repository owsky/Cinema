import Fastify, { FastifyInstance } from "fastify"
import logger from "../logger"
import authentication from "../plugins/authentication"
import routes from "../routes"

export default async function createServer(): Promise<FastifyInstance> {
  const fastify = Fastify({
    logger: logger,
  })
  await fastify.register(authentication)
  await fastify.register(routes)
  return fastify
}
