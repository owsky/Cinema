import { FastifyPluginAsync, FastifyRequest } from "fastify"
import userGetHandler from "./userGetHandler"
import userPutHandler from "./userPutHandler"

const route: FastifyPluginAsync = async (fastify, _opts) => {
  const postgres = fastify.pg

  fastify.route({
    method: "GET",
    url: "/",
    handler: async (
      request: FastifyRequest<{ Querystring: { email: string } }>,
      reply
    ) => userGetHandler(request, reply, postgres),
    schema: {
      querystring: {
        email: {
          type: "string",
        },
      },
      response: {
        200: {
          type: "object",
          properties: {
            email: {
              type: "string",
            },
            full_name: {
              type: "string",
            },
            user_role: {
              type: "string",
            },
          },
        },
      },
    },
  })

  fastify.route({
    method: "PUT",
    url: "/",
    handler: async (
      request: FastifyRequest<{
        Body: { email: string; password: string; full_name: string }
      }>,
      reply
    ) => {
      userPutHandler(request, reply, postgres, fastify.config.SECRET)
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
