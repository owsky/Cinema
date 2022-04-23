import { FastifyReply, FastifyRequest, HookHandlerDoneFunction } from "fastify"
import verifyToken from "../utils/verifyToken"

export default function authenticationHook(
  request: FastifyRequest,
  reply: FastifyReply,
  done: HookHandlerDoneFunction
) {
  if (request.headers.authorization) {
    const token = request.headers.authorization
    if (verifyToken(token)) done()
    else void reply.code(403).send({ error: "Forbidden" })
  } else {
    void reply.code(401).send({ error: "Authentication required" })
  }
}
