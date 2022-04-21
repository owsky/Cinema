import { Static, Type } from "@sinclair/typebox"
import { FastifyPluginAsync, FastifyRequest } from "fastify"
import config from "../../config/setupEnvinronment"
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
  user_role: Type.Optional(Type.String()),
})
export type UserType = Static<typeof User>
const UserWithPassword = Type.Object({
  email: Type.String(),
  full_name: Type.String(),
  password: Type.String(),
  user_role: Type.Optional(Type.String()),
})
export type UserWithPasswordType = Static<typeof UserWithPassword>

const route: FastifyPluginAsync = async (fastify, _opts) => {
  fastify.route({
    method: "GET",
    url: "/",
    handler: async (
      request: FastifyRequest<{ Querystring: EmailType }>,
      reply
    ) => userGetHandler(request, reply),
    schema: {
      querystring: {
        Email,
      },
      response: {
        200: User,
      },
    },
  })

  fastify.route({
    method: "PUT",
    url: "/",
    handler: async (
      request: FastifyRequest<{
        Body: UserWithPasswordType
      }>,
      reply
    ) => {
      userPutHandler(request, reply, config.SECRET)
    },
    schema: {
      body: UserWithPassword,
    },
  })
}

export default route
