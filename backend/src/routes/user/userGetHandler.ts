import { FastifyReply, FastifyRequest } from "fastify"
import { PostgresDb } from "fastify-postgres"
import usersMethodsImpl from "../../db/users/usersMethodsImpl"

const userGetHandler = async (
  request: FastifyRequest<{ Querystring: { email: string } }>,
  reply: FastifyReply,
  postgres: PostgresDb & Record<string, PostgresDb>
) => {
  const email = request.query.email
  try {
    const user = await usersMethodsImpl.getUser(postgres, email)
    if (!user) reply.code(404).send({ message: "User not found" })
    reply.send(user)
  } catch (e) {
    console.error(e)
    reply.code(400).send({ message: "Error" })
  }
}
export default userGetHandler
