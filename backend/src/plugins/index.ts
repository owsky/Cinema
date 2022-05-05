import fastifyRateLimit from "@fastify/rate-limit"
import { FastifyInstance } from "fastify"
import config from "../config"
import authentication from "./authentication"
import fastifySwagger from "@fastify/swagger"
import fastifyCors from "@fastify/cors"

export default async function registerPlugins(fastify: FastifyInstance) {
  await fastify.register(authentication, { secret: config.SECRET })
  await fastify.register(fastifyCors, {
    origin: "*",
  })
  await fastify.register(fastifyRateLimit, {
    max: 100,
    timeWindow: "10 minutes",
  })
  await fastify.register(fastifySwagger, {
    routePrefix: "/docs",
    swagger: {
      info: {
        title: "Cinema but Fast",
        description: "Routes definitions for the Cinema but Fast API",
        version: "1.0.0",
      },
      host: "localhost:3000",
      schemes: ["http"],
      consumes: ["application/json"],
      produces: ["application/json"],
    },
    exposeRoute: true,
  })
}
