import { FastifyPluginAsync } from "fastify"
import userRoute from "./user"
import loginRoute from "./login"
import signupRoute from "./signup"
import moviesRoute from "./movies"
import ticketsRoute from "./tickets"
import searchRoute from "./search"
import actorsRoutes from "./actors"

const routes: FastifyPluginAsync = async (fastify, _opts) => {
  await Promise.all([
    fastify.register(userRoute, { prefix: "/user" }),
    fastify.register(loginRoute, { prefix: "/login" }),
    fastify.register(signupRoute, { prefix: "/signup" }),
    fastify.register(moviesRoute, { prefix: "/movies" }),
    fastify.register(ticketsRoute, { prefix: "/tickets" }),
    fastify.register(searchRoute, { prefix: "/search" }),
    fastify.register(actorsRoutes, { prefix: "/actors" }),
  ])
}

export default routes
