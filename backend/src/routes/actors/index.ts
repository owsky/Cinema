import { Static, Type } from "@sinclair/typebox"
import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { Actor } from "../../models/Actor"
import { ErrorResponse } from "../ErrorTypebox"
import actorsGetHandler from "./actorsGetHandler"

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  const ActorQuery = Type.Object({
    actor_id: Type.Number(),
  })
  type ActorQueryType = Static<typeof ActorQuery>

  fastify.route({
    method: "GET",
    url: "/",
    handler: async (
      request: FastifyRequest<{ Querystring: ActorQueryType }>,
      reply
    ) => {
      try {
        const actor = await actorsGetHandler(request.query.actor_id)
        request.log.info(actor)
        if (actor) void reply.code(200).send(actor)
        else void reply.code(404).send({ error: "Actor not found" })
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      querystring: ActorQuery,
      response: {
        200: Actor,
        404: ErrorResponse,
        500: ErrorResponse,
      },
    },
  })

  done()
}

export default routes
