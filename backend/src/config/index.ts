import { FastifyInstance } from "fastify"
import dbConnect from "./dbConnect"
import setupEnvironment from "./fastifyEnv"

export default async function config(fastify: FastifyInstance) {
  await setupEnvironment(fastify)
  dbConnect(fastify)
  fastify.ready(async err => {
    if (err) fastify.log.error(err)
    else {
      fastify.log.info("Fastify config completed successfully")
    }
  })
}
