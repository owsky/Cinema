import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { DatabaseError } from "pg"
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
          await reply
            .code(400)
            .send({ error: "The provided email address is already in use" })
        void reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      body: Signup,
    },
  })

  done()
}

export default route
