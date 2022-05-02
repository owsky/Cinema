import { Type } from "@sinclair/typebox"
import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { Projection } from "../../../models/Projection"
import { ErrorResponse } from "../../ErrorTypebox"
import movieScheduleGetHandler from "./handlers/movieScheduleGetHandler"
import scheduleGetHandler from "./handlers/scheduleGetHandler"
import { MovieParams, MovieParamsType } from "../typebox/MovieParams"
import { ScheduleQueryType, ScheduleQuery } from "./typebox/ScheduleQuery"
import postgres from "../../../db"
import {
  MovieSchedulePostBody,
  MovieSchedulePostBodyType,
} from "./typebox/MovieSchedulePostParams"
import { SuccessResponse } from "../../SuccessTypebox"
import {
  ProjectionDeleteParams,
  ProjectionDeleteParamsType,
} from "./typebox/projectionDeleteParams"

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "GET",
    url: "/",
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
    method: "POST",
    url: "/",
    onRequest: [fastify.authentication.adminAuthHook],
    handler: async (request, reply) => {
      const typedRequest = request as FastifyRequest<{
        Body: MovieSchedulePostBodyType
      }>
      try {
        await postgres.moviesMethods.addToSchedule(
          typedRequest.body.movie_id,
          typedRequest.body.start_date,
          typedRequest.body.price,
          typedRequest.body.room
        )
        void reply.code(200).send({ message: "Movie added to schedule" })
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Couldn't add movie to schedule" })
      }
    },
    schema: {
      body: MovieSchedulePostBody,
      response: {
        200: SuccessResponse,
        500: ErrorResponse,
      },
    },
  })

  fastify.route({
    method: "DELETE",
    url: "/:projectionId",
    onRequest: [fastify.authentication.adminAuthHook],
    handler: async (request, reply) => {
      const typedRequest = request as FastifyRequest<{
        Params: ProjectionDeleteParamsType
      }>
      try {
        await postgres.moviesMethods.removeFromSchedule(
          typedRequest.params.projectionId
        )
        void reply
          .code(200)
          .send({ message: "Projection deleted successfully" })
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Couldn't delete projection" })
      }
    },
    schema: {
      params: ProjectionDeleteParams,
      response: {
        200: SuccessResponse,
        500: ErrorResponse,
      },
    },
  })

  fastify.route({
    method: "GET",
    url: "/:movieId",
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
