import { FastifyReply, FastifyRequest } from "fastify"
import { EmailType } from "."
import usersMethodsImpl from "../../db/users/usersMethodsImpl"

const userGetHandler = async (
  request: FastifyRequest<{ Querystring: EmailType }>,
  reply: FastifyReply
) => {
  const email = request.query.email
  try {
    const user = await usersMethodsImpl.getUser(email)
    if (!user) reply.code(404).send({ message: "User not found" })
    reply.send(user)
  } catch (e) {
    console.error(e)
    reply.code(400).send({ message: "Error" })
  }
}
export default userGetHandler
