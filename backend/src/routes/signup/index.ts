import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { DatabaseError } from "pg"
import { ErrorResponse } from "../ErrorTypebox"
import { SuccessResponse } from "../SuccessTypebox"
import signupHandler from "./signupHandler"
import { Signup, SignupType } from "./SignupTypebox"

const route: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "POST",
    url: "/",
    handler: async (
      request: FastifyRequest<{
        Body: SignupType
      }>,
      reply
    ) => {
      try {
        await signupHandler(
          request.body.email,
          request.body.full_name,
          request.body.password
        )
        void reply.code(201).send({ message: "User created successfully" })
      } catch (e) {
        request.log.error(e)
        if (e instanceof DatabaseError && e.code === "23505")
          void reply
            .code(400)
            .send({ error: "The provided email address is already in use" })
        else void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      body: Signup,
      response: {
        201: SuccessResponse,
        400: ErrorResponse,
        500: ErrorResponse,
      },
    },
  })

  done()
}

export default route
