import Fastify, { FastifyInstance } from "fastify"
import fastifyRateLimit from "@fastify/rate-limit"
import logger from "../logger"
import authentication from "../plugins/authentication"
import routes from "../routes"
import config from "../config"

export default async function createServer(): Promise<FastifyInstance> {
  const fastify = Fastify({
    logger: logger,
  })
  await fastify.register(authentication, { secret: config.SECRET })
  await fastify.register(fastifyRateLimit, {
    max: 100,
    timeWindow: "10 minutes",
  })
  await fastify.register(routes)
  return fastify
}
