import { FastifyReply, FastifyRequest } from "fastify"
import { PostgresDb } from "fastify-postgres"
import usersMethodsImpl from "../../db/users/usersMethodsImpl"

const userPutController = async (
  request: FastifyRequest<{
    Body: { email: string; password: string; full_name: string }
  }>,
  reply: FastifyReply,
  postgres: PostgresDb & Record<string, PostgresDb>
) => {
  try {
    await usersMethodsImpl.createUser(
      postgres,
      request.body.email,
      request.body.full_name,
      request.body.password
    )
    reply.code(200).send({ message: "User created successfully" })
  } catch (e) {
    console.error(e)
    reply.code(500).send({ error: "Couldn't create the user" })
  }
}
export default userPutController
