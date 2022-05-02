import { FastifyPluginCallback, onRequestAsyncHookHandler } from "fastify"
import { JwtPayload } from "jsonwebtoken"

export interface JsonWebToken {
  email: string
  fullName: string
  userRole: string
}

export interface PluginOptions {
  secret: string
}

export interface AuthenticationMethods {
  userAuthHook: onRequestAsyncHookHandler
  adminAuthHook: onRequestAsyncHookHandler
  passwordUtils: {
    createPassword: (
      plaintextPassword: string,
      salt?: string
    ) => Promise<{ password: string; salt: string } | null>
    verifyPassword: (
      hash: string,
      plaintextPassword: string,
      salt: string
    ) => Promise<boolean>
  }
  jwtUtils: {
    verifyToken: (token: string) => string | JwtPayload | undefined
    signToken: (email: string, fullName: string, userRole: string) => string
  }
}

declare module "fastify" {
  interface FastifyInstance {
    authentication: AuthenticationMethods
  }

  interface FastifyRequest {
    user: JsonWebToken
    verifyToken: (token: string) => string | JwtPayload | undefined
  }
}

export const cinemaAuthenticationPlugin: FastifyPluginCallback<PluginOptions>

export default cinemaAuthenticationPlugin
