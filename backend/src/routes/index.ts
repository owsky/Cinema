import { FastifyPluginAsync } from "fastify"
import userRoute from "./user"

const routes: FastifyPluginAsync = async (fastify, _opts) => {
  fastify.register(userRoute, { prefix: "/user" })
}

export default routes
