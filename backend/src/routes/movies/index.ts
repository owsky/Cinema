import { FastifyPluginCallback, FastifyRequest } from "fastify"
import scheduleGetHandler from "./handlers/scheduleGetHandler"
import { Type } from "@sinclair/typebox"
import { ErrorResponse } from "../ErrorTypebox"
import { Projection } from "../../models/Projection"
import getMovieHandler from "./handlers/movieParamGetHandler"
import { Movie } from "../../models/Movie"
import getAllMoviesHandler from "./handlers/movieGetHandler"
import { MovieParams, MovieParamsType } from "./movieParams"
import getMovieSchedule from "../../db/moviesMethods/getMovieSchedule"

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "GET",
    url: "/",
    handler: async (request, reply) => {
      try {
        void reply.code(200).send(await getAllMoviesHandler())
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Internal server error" })
      }
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
        void reply.code(400).send({ error: "Missing movie ID parameter" })
      else
        try {
          const movie = await getMovieHandler(movieId)
          if (movie) void reply.code(200).send(movie)
          else void reply.code(404).send({ error: "Movie not found" })
        } catch (e) {
          request.log.error(e)
          void reply.code(500).send({ error: "Internal server error" })
        }
    },
    schema: {
      params: MovieParams,
      response: {
        200: Movie,
        404: ErrorResponse,
        500: ErrorResponse,
      },
    },
  })

  fastify.route({
    method: "GET",
    url: "/:movieId/schedule",
    handler: async (
      request: FastifyRequest<{ Params: MovieParamsType }>,
      reply
    ) => {
      const movieId = request.params.movieId
      if (!movieId)
        void reply.code(400).send({ error: "Missing movie ID in parameter" })
      else
        try {
          const schedule = await getMovieSchedule(movieId)
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
        404: ErrorResponse,
        500: ErrorResponse,
      },
    },
  })

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
    url: "/schedule/week",
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
