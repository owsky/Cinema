import { FastifyPluginCallback, FastifyRequest } from "fastify"
import scheduleGetHandler from "./handlers/scheduleGetHandler"
import { Static, Type } from "@sinclair/typebox"
import { ErrorResponse } from "../ErrorTypebox"
import { Projection } from "../../models/Projection"
import getMovieHandler from "./handlers/movieParamGetHandler"
import { Movie } from "../../models/Movie"
import { MovieParams, MovieParamsType } from "./MovieParams"
import movieScheduleGetHandler from "./handlers/movieScheduleGetHandler"
import { SuccessResponse } from "../SuccessTypebox"
import postgres from "../../db"
import { DatabaseError } from "pg"

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  const MoviePostBody = Type.Object({
    Title: Type.String(),
    Year: Type.String(),
    Runtime: Type.String(),
    Genre: Type.String(),
    Director: Type.String(),
    Plot: Type.String(),
    Actors: Type.String(),
  })
  type MoviePostBodyType = Static<typeof MoviePostBody>

  fastify.route({
    method: "POST",
    url: "/",
    handler: async (request, reply) => {
      try {
        const req = request as FastifyRequest<{ Body: MoviePostBodyType }>
        await postgres.moviesMethods.insertNewMovie(
          req.body.Title,
          req.body.Year,
          req.body.Runtime,
          req.body.Genre,
          req.body.Director,
          req.body.Plot,
          req.body.Actors.split(", ")
        )
        void reply.code(200).send({ message: "Movie inserted correctly" })
      } catch (e) {
        request.log.error(e)
        if (e instanceof DatabaseError && e.code === "P0001")
          void reply
            .code(400)
            .send({ error: "Movie already saved in the dabase" })
        else void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      body: MoviePostBody,
      response: {
        200: SuccessResponse,
        400: ErrorResponse,
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
        "4xx": ErrorResponse,
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

  const ScheduleQuery = Type.Object({
    currentWeek: Type.Optional(Type.Boolean()),
  })
  type ScheduleQueryType = Static<typeof ScheduleQuery>

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

  done()
}

export default routes
