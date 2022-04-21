import { FastifyReply, FastifyRequest } from "fastify"
import { UserWithPasswordType } from "."
import postgres from "../../db"
import createPassword from "../../utils/createPassword"
import generateSalt from "../../utils/generateSalt"

const userPutHandler = async (
  request: FastifyRequest<{
    Body: UserWithPasswordType
  }>,
  reply: FastifyReply,
  secret: string
) => {
  try {
    const salt = await generateSalt()
    if (salt) {
      const password = await createPassword(request.body.password, salt, secret)
      if (password) {
        await postgres.usersMethods.createUser(
          request.body.email,
          request.body.full_name,
          request.body.password,
          salt
        )
      }
    }
    reply.code(200).send({ message: "User created successfully" })
  } catch (e: any) {
    request.log.error(e)
    if (e.code === "23505")
      reply
        .code(400)
        .send({ error: "The provided email address is already in use" })
    reply.code(500).send({ error: e.message })
  }
}
export default userPutHandler
