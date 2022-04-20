import { Static, Type } from "@sinclair/typebox"
import { FastifyPluginAsync, FastifyRequest } from "fastify"
import User from "../../models/user"
import userGetHandler from "./userGetHandler"
import userPutHandler from "./userPutHandler"

const Email = Type.Object({
  email: Type.String({ format: "email" }),
})
export type EmailType = Static<typeof Email>

const User = Type.Object({
  email: Type.String(),
  full_name: Type.String(),
  password: Type.String(),
  user_role: Type.String(),
})
export type UserType = Static<typeof User>

const route: FastifyPluginAsync = async (fastify, _opts) => {
  const postgres = fastify.pg

  fastify.route({
    method: "GET",
    url: "/",
    handler: async (
      request: FastifyRequest<{ Querystring: EmailType }>,
      reply
    ) => userGetHandler(request, reply, postgres),
    schema: {
      querystring: {
        Email,
      },
      response: {
        200: {
          type: "object",
          properties: {
            email: { type: "string" },
            full_name: { type: "string" },
            user_role: { type: "string" },
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
        Body: UserType
      }>,
      reply
    ) => {
      userPutHandler(request, reply, postgres, fastify.config.SECRET)
    },
    schema: {
      body: User,
    },
  })
}

export default route
