import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { DatabaseError } from "pg"
import { Email, EmailType } from "./emailTypebox"
import userGetHandler from "./userGetHandler"
import userPutHandler from "./userPutHandler"
import { User, UserWithPassword, UserWithPasswordType } from "./userTypebox"

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
        if (!user) await reply.code(404).send({ error: "User not found" })
        else await reply.send(user)
      } catch (e) {
        request.log.error(e)
        await reply.code(500).send({ error: "Internal server error" })
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

  fastify.route({
    method: "PUT",
    url: "/",
    handler: async (
      request: FastifyRequest<{
        Body: UserWithPasswordType
      }>,
      reply
    ) => {
      try {
        await userPutHandler(
          request.body.email,
          request.body.full_name,
          request.body.password
        )
        await reply.code(200).send({ message: "User created successfully" })
      } catch (e) {
        request.log.error(e)
        if (e instanceof DatabaseError && e.code === "23505")
          await reply
            .code(400)
            .send({ error: "The provided email address is already in use" })
        await reply.code(500).send({ error: "Internal server error" })
      }
    },
    schema: {
      body: UserWithPassword,
    },
  })

  done()
}

export default route
