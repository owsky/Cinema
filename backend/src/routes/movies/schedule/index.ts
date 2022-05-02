import { Type } from "@sinclair/typebox"
import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { Projection } from "../../../models/Projection"
import { ErrorResponse } from "../../ErrorTypebox"
import movieScheduleGetHandler from "./handlers/movieScheduleGetHandler"
import scheduleGetHandler from "./handlers/scheduleGetHandler"
import { MovieParams, MovieParamsType } from "../typebox/MovieParams"
import { ScheduleQueryType, ScheduleQuery } from "./ScheduleQuery"

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "GET",
    url: "/schedule",
    handler: async (
      request: FastifyRequest<{ Querystring: ScheduleQueryType }>,
      reply
    ) => {
      try {
        const schedule = await scheduleGetHandler(request.query.currentWeek)
        void reply.code(200).send(schedule)
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Failed to retrieve the schedule" })
      }
    },
    schema: {
      querystring: ScheduleQuery,
      response: {
        200: Type.Array(Projection),
        500: ErrorResponse,
      },
    },
  })

  fastify.route({
    method: "GET",
    url: "/schedule/:movieId/",
    handler: async (
      request: FastifyRequest<{ Params: MovieParamsType }>,
      reply
    ) => {
      const movieId = request.params.movieId
      if (!movieId)
        void reply.code(400).send({ error: "Missing movie ID in parameter" })
      else
        try {
          const schedule = await movieScheduleGetHandler(movieId)
          if (schedule) void reply.code(200).send(schedule)
          else void reply.code(404).send({ error: "Movie not found" })
        } catch (e) {
          request.log.error(e)
          void reply.code(500).send({ error: "Internal server error" })
        }
    },
    schema: {
      params: MovieParams,
      response: {
        200: Type.Array(Projection),
        "4xx": ErrorResponse,
        500: ErrorResponse,
      },
    },
  })

  done()
}
export default routes
