import { onRequestAsyncHookHandler } from "fastify"
import postgres from "../../db"
import { JsonWebToken } from "./authentication"
import verifyToken from "./verifyJWT"

const onRequestHook: onRequestAsyncHookHandler = async (request, reply) => {
  const token = request.headers.authorization
  if (token) {
    const payload = verifyToken(token)
    if (payload) {
      const userToken = payload as JsonWebToken
      const user = await postgres.usersMethods.getUser(userToken.email)
      if (user) {
        request.user = {
          email: user.email,
          fullName: user.full_name,
          userRole: user.user_role,
        }
      } else {
        void reply.code(403).send({ error: "Forbidden" })
      }
    } else {
      void reply.code(401).send({ error: "Invalid Json Web Token supplied" })
    }
  } else {
    void reply.code(401).send({ error: "Authentication required" })
  }
}
export default onRequestHook
