import { FastifyPluginCallback } from "fastify"
import fastifyPlugin from "fastify-plugin"
import { AuthenticationMethods, PluginOptions } from "./authentication"
import onRequestHook from "./onRequestHook"
import {
  createPassword as createPasswordMethod,
  verifyPassword as verifyPasswordMethod,
  signToken as signTokenMethod,
} from "./utils"
import { default as verifyTokenMethod } from "./utils/verifyJWT"

const authPlugin: FastifyPluginCallback<PluginOptions> = (
  fastify,
  opts,
  done
) => {
  if (!opts.secret) throw new Error("No secret was declare in plugin options")
  const exports: AuthenticationMethods = {
    authenticationHook: onRequestHook,
    passwordUtils: {
      createPassword: (plaintextPassword: string, salt?: string) =>
        createPasswordMethod(plaintextPassword, opts.secret, salt),
      verifyPassword: (hash: string, plaintextPassword: string, salt: string) =>
        verifyPasswordMethod(hash, plaintextPassword, salt, opts.secret),
    },
    jwtUtils: {
      verifyToken: (token: string) => verifyTokenMethod(token, opts.secret),
      signToken: (email: string, fullName: string, userRole: string) =>
        signTokenMethod(email, fullName, userRole, opts.secret),
    },
  }
  fastify.decorate("authentication", exports)
  fastify.decorateRequest("verifyToken", (token: string) =>
    verifyTokenMethod(token, opts.secret)
  )

  done()
}

export default fastifyPlugin(authPlugin, {
  fastify: "3.x",
  name: "cinema-authentication-plugin",
})
