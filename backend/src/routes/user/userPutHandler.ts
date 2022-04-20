import { FastifyReply, FastifyRequest } from "fastify"
import { PostgresDb } from "fastify-postgres"
import usersMethodsImpl from "../../db/users/usersMethodsImpl"
import createPassword from "../../utils/createPassword"
import generateSalt from "../../utils/generateSalt"

const userPutHandler = async (
  request: FastifyRequest<{
    Body: { email: string; password: string; full_name: string }
  }>,
  reply: FastifyReply,
  postgres: PostgresDb & Record<string, PostgresDb>,
  secret: string
) => {
  try {
    const salt = await generateSalt()
    if (salt) {
      const password = await createPassword(request.body.password, salt, secret)
      if (password) {
        await usersMethodsImpl.createUser(
          postgres,
          request.body.email,
          request.body.full_name,
          password,
          salt
        )
      }
    }
    reply.code(200).send({ message: "User created successfully" })
  } catch (e) {
    console.error(e)
    reply.code(500).send({ error: "Couldn't create the user" })
  }
}
export default userPutHandler
