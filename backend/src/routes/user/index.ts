import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { Email, EmailType } from "./emailTypebox"
import userGetHandler from "./userGetHandler"
import { User } from "./userTypebox"

const route: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "GET",
    url: "/",
    handler: async (
      request: FastifyRequest<{ Querystring: EmailType }>,
      reply
    ) => {
      const email = request.query.email
      try {
        const user = await userGetHandler(email)
        if (!user) void reply.code(404).send({ error: "User not found" })
        else void reply.send(user)
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      querystring: {
        Email,
      },
      response: {
        200: User,
      },
    },
  })
  done()
}

export default route
