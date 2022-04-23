import { FastifyPluginCallback, FastifyRequest } from "fastify"
import loginHandler from "./loginHandler"
import { Login, LoginType } from "./loginTypebox"

const route: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "POST",
    url: "/",
    handler: async (request: FastifyRequest<{ Body: LoginType }>, reply) => {
      try {
        const token = await loginHandler(
          request.body.email,
          request.body.password
        )
        if (token)
          void reply.code(200).send({ message: "Login successful", token })
        else void reply.code(401).send({ error: "Authentication failed" })
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      body: Login,
      response: {
        200: {
          message: { type: "string" },
          token: { type: "string" },
        },
        403: {
          error: { type: "string" },
        },
        500: { error: { type: "string" } },
      },
    },
  })

  done()
}
export default route
