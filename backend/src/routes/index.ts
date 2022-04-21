import { FastifyPluginAsync } from "fastify"
import userRoute from "./user"
import loginRoute from "./login"

const routes: FastifyPluginAsync = async (fastify, _opts) => {
  await Promise.all([
    fastify.register(userRoute, { prefix: "/user" }),
    fastify.register(loginRoute, { prefix: "/login" }),
  ])
}

export default routes
