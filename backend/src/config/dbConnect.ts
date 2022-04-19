import { FastifyInstance } from "fastify"
import fastifyPostgres from "fastify-postgres"

export default function dbConnect(fastify: FastifyInstance) {
  fastify.register(fastifyPostgres, {
    connectionString: `postgresql://${fastify.config.DB_USER}:${fastify.config.DB_PASSWORD}@${fastify.config.DB_HOST}:${fastify.config.DB_PORT}/Cinema`,
  })
}
