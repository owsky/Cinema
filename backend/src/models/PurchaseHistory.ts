import { Static, Type } from "@sinclair/typebox"

export const PurchaseHistory = Type.Object({
  title: Type.String(),
  start_date: Type.String(),
  room: Type.String(),
  seat: Type.Number(),
})
export type PurchaseHistoryType = Static<typeof PurchaseHistory>
