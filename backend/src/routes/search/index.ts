import { Type, Static } from "@sinclair/typebox"
import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { ErrorResponse } from "../ErrorTypebox"
import searchHandler from "./searchHandler"

const SearchQuery = Type.Object({
  input: Type.String(),
})
type SearchQueryType = Static<typeof SearchQuery>

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "GET",
    url: "/",
    handler: async (
      request: FastifyRequest<{ Querystring: SearchQueryType }>,
      reply
    ) => {
      try {
        const results = await searchHandler(request.query.input)
        void reply.code(200).send(results)
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Search failed" })
      }
    },
    schema: {
      querystring: SearchQuery,
      response: {
        200: Type.Array(Type.String()),
        500: ErrorResponse,
      },
    },
  })

  done()
}

export default routes
