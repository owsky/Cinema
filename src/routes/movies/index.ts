import { FastifyPluginAsync, FastifyRequest } from "fastify"
import { ErrorResponse } from "../ErrorTypebox"
import { Movie } from "../../models/Movie"
import { MovieParams, MovieParamsType } from "./typebox/MovieParams"
import { SuccessResponse } from "../SuccessTypebox"
import postgres from "../../db"
import { DatabaseError } from "pg"
import { MoviePostBody, MoviePostBodyType } from "./typebox/MoviePostBody"
import scheduleRoutes from "./schedule"

const movies: FastifyPluginAsync = async (fastify, _opts) => {
  await fastify.register(scheduleRoutes, { prefix: "/schedule" })
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
          req.body.Actors
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
          const movie = await postgres.moviesMethods.getMovie(movieId)
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
    method: "DELETE",
    url: "/:movieId",
    onRequest: [fastify.authentication.adminAuthHook],
    handler: async (request, reply) => {
      const movieId = (request as FastifyRequest<{ Params: MovieParamsType }>)
        .params.movieId
      if (!movieId)
        void reply.code(400).send({ error: "Missing movie ID parameter" })
      else
        try {
          const success = await postgres.moviesMethods.removeMovie(movieId)
          if (!success)
            void reply
              .code(400)
              .send({ error: "Trying to delete a non-existent movie" })
          else
            void reply.code(200).send({ message: "Movie deleted succesfully" })
        } catch (e) {
          request.log.error(e)
          void reply.code(500).send({ error: "Internal server error" })
        }
    },
    schema: {
      params: MovieParams,
      response: {
        200: SuccessResponse,
        500: ErrorResponse,
      },
    },
  })
}

export default movies
