import { Static, Type } from "@sinclair/typebox"
import { FastifyPluginCallback, FastifyRequest } from "fastify"
import authenticationHook from "../../hooks/authenticationHook"
import purchaseTicketHandler from "./handlers/purchaseTicketHandler"

const TicketPurchaseBody = Type.Object({
  user_email: Type.String(),
  projection_id: Type.Number(),
  seat_code: Type.Array(Type.Number()),
})
type TicketPurchaseBodyType = Static<typeof TicketPurchaseBody>

const routes: FastifyPluginCallback = (fastify, _opts, done) => {
  fastify.route({
    method: "POST",
    url: "/",
    onRequest: (
      request: FastifyRequest<{ Body: TicketPurchaseBodyType }>,
      reply,
      done
    ) => {
      const authenticated = authenticationHook(request.headers.authorization)
      if (authenticated) done()
      else void reply.code(401).send({ error: "Authentication required" })
    },
    handler: async (
      request: FastifyRequest<{ Body: TicketPurchaseBodyType }>,
      reply
    ) => {
      try {
        const success = await purchaseTicketHandler(
          request.body.user_email,
          request.body.projection_id,
          request.body.seat_code
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
    },
  })

  done()
}
export default routes
