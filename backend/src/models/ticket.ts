import { Type } from "@sinclair/typebox"
import { User } from "./User"
import { Projection } from "./Projection"

export const Ticket = Type.Object({
  user: User,
  projection: Projection,
})
