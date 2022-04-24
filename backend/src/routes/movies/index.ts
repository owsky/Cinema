import { FastifyPluginCallback } from "fastify"
import scheduleGetHandler from "./scheduleGetHandler"
import { Type } from "@sinclair/typebox"
import { ErrorResponse } from "../ErrorTypebox"
import { Projection } from "../../models/Projection"

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "GET",
    url: "/schedule",
    handler: async (request, reply) => {
      try {
        const schedule = await scheduleGetHandler()
        void reply.code(200).send(schedule)
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Failed to retrieve the schedule" })
      }
    },
    schema: {
      response: {
        200: Type.Array(Projection),
        500: ErrorResponse,
      },
    },
  })

  fastify.route({
    method: "GET",
    url: "/schedule/currentweek",
    handler: async (request, reply) => {
      try {
        const schedule = await scheduleGetHandler(true)
        void reply.code(200).send(schedule)
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Failed to retrieve the schedule" })
      }
    },
    schema: {
      response: {
        200: Type.Array(Projection),
        500: ErrorResponse,
      },
    },
  })

  done()
}

export default routes
