import { onRequestHookHandler } from "fastify"

export interface JsonWebToken {
  email: string
  fullName: string
  userRole: string
}

declare module "fastify" {
  interface FastifyInstance {
    jwtAuth: onRequestHookHandler
  }
  interface FastifyRequest {
    user: JsonWebToken
  }
}
