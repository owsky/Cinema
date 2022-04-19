import { FastifyPluginAsync, FastifyRequest } from "fastify"
import userGetController from "../../controllers/user/userGetController"
import userPutController from "../../controllers/user/userPutController"

const route: FastifyPluginAsync = async (fastify, _opts) => {
  const postgres = fastify.pg

  fastify.route({
    method: "GET",
    url: "/user",
    handler: async (
      request: FastifyRequest<{ Querystring: { email: string } }>,
      reply
    ) => userGetController(request, reply, postgres),
    schema: {
      querystring: {
        email: {
          type: "string",
        },
      },
    },
  })

  fastify.route({
    method: "PUT",
    url: "/user",
    handler: async (
      request: FastifyRequest<{
        Body: { email: string; password: string; full_name: string }
      }>,
      reply
    ) => {
      userPutController(request, reply, postgres)
    },
    schema: {
      body: {
        type: "object",
        properties: {
          email: {
            type: "string",
            require: true,
          },
          full_name: {
            type: "string",
            require: true,
          },
          password: {
            type: "string",
            require: true,
          },
        },
      },
    },
  })
}

export default route
