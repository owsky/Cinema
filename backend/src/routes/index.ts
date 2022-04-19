import { FastifyPluginAsync } from "fastify"
import userRoute from "./user"

const routes: FastifyPluginAsync = async (fastify, _opts) => {
  fastify.register(userRoute)
}

export default routes
