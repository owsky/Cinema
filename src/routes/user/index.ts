import { FastifyPluginCallback } from "fastify"
import postgres from "../../db"
import { ErrorResponse } from "../ErrorTypebox"
import { SuccessResponse } from "../SuccessTypebox"

const route: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "DELETE",
    url: "/",
    onRequest: [fastify.authentication.userAuthHook],
    handler: async (request, reply) => {
      try {
        await postgres.usersMethods.deleteUser(request.user.email)
        void reply
          .code(200)
          .send({ message: "User account deleted successfully" })
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      response: {
        200: SuccessResponse,
        404: ErrorResponse,
        500: ErrorResponse,
      },
    },
  })

  done()
}

export default route
