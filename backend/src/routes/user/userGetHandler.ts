import { FastifyReply, FastifyRequest } from "fastify"
import { EmailType } from "."
import postgres from "../../db/index"
import logger from "../../logger"

const userGetHandler = async (
  request: FastifyRequest<{ Querystring: EmailType }>,
  reply: FastifyReply
) => {
  const email = request.query.email
  logger.info(email)
  try {
    const user = await postgres.usersMethods.getUser(email)
    if (!user) reply.code(404).send({ message: "User not found" })
    reply.send(user)
  } catch (e: any) {
    request.log.error(e)
    reply.code(500).send({ error: "Internal server error" })
  }
}
export default userGetHandler
