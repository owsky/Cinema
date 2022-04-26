import { FastifyPluginCallback } from "fastify"
import fastifyPlugin from "fastify-plugin"
import onRequestHook from "./onRequestHook"

const authPlugin: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.decorate("jwtAuth", onRequestHook)
  done()
}

export default fastifyPlugin(authPlugin)
