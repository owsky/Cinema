import { Type } from "@sinclair/typebox"
import { FastifyPluginCallback, FastifyRequest } from "fastify"
import { ErrorResponse } from "../ErrorTypebox"
import { SuccessResponse } from "../SuccessTypebox"
import purchaseHistoryHandler from "./handlers/purchaseHistoryHandler"
import purchaseTicketHandler from "./handlers/purchaseTicketHandler"
import {
  TicketPurchaseBodyType,
  TicketPurchaseBody,
} from "./typebox/TicketPurchaseBody"

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "GET",
    url: "/",
    onRequest: [fastify.authentication.authenticationHook],
    handler: async (request, reply) => {
      try {
        const history = await purchaseHistoryHandler(request.user.email)
        void reply.code(200).send(history)
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Couldn't purchase the ticket" })
      }
    },
    schema: {
      response: {
        200: Type.Array(
          Type.Object({
            title: Type.String(),
            start_date: Type.String(),
            room: Type.String(),
            seat: Type.Integer(),
          })
        ),
        500: ErrorResponse,
      },
    },
  })

  fastify.route({
    method: "POST",
    url: "/",
    onRequest: [fastify.authentication.authenticationHook],
    handler: async (request, reply) => {
      try {
        const typedRequest = request as FastifyRequest<{
          Body: TicketPurchaseBodyType
        }>
        const success = await purchaseTicketHandler(
          typedRequest.user.email,
          typedRequest.body.projection_id,
          typedRequest.body.seat_code
        )
        if (success)
          void reply.code(200).send({ message: "Ticket purchased correctly" })
        else
          void reply.code(500).send({ error: "Couldn't purchase the ticket" })
      } catch (e) {
        request.log.error(e)
        void reply.code(500).send({ error: "Couldn't purchase the ticket" })
      }
    },
    schema: {
      body: TicketPurchaseBody,
      response: {
        200: SuccessResponse,
        500: ErrorResponse,
      },
    },
  })

  done()
}
export default routes
