import { Static, Type } from "@sinclair/typebox"

export const Seat = Type.Object({
  code: Type.Integer(),
})

export const Room = Type.Object({
  name: Type.String(),
  seats: Type.Array(Seat),
})
export type RoomType = Static<typeof Room>
