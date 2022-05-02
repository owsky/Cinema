import { Type, Static } from "@sinclair/typebox"

export const TicketPurchaseBody = Type.Object({
  user_email: Type.String(),
  projection_id: Type.Number(),
  seat_code: Type.Array(Type.Number()),
})
export type TicketPurchaseBodyType = Static<typeof TicketPurchaseBody>
