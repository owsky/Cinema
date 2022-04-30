import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { ErrorResponse } from "../ErrorTypebox"
import { LoginRequest, LoginRequestType, LoginResponse } from "./loginTypebox"
import loginHandler from "./loginHandler"

const route: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "POST",
    url: "/",
    handler: async (
      request: FastifyRequest<{ Body: LoginRequestType }>,
      reply
    ) => {
      try {
        const token = await loginHandler(
          fastify.authentication.passwordUtils.createPassword,
          fastify.authentication.jwtUtils.signToken,
          request.body.email,
          request.body.password
        )
        if (token)
          void reply.code(200).send({
            message: "Login successful",
            token: token,
          })
        else void reply.code(401).send({ error: "Authentication failed" })
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      body: LoginRequest,
      response: {
        200: LoginResponse,
        401: ErrorResponse,
        500: ErrorResponse,
      },
    },
  })

  done()
}
export default route
