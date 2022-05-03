import { Static, Type } from "@sinclair/typebox"

export const MovieScheduleBody = Type.Object({
  movie_id: Type.Number(),
  start_date: Type.String(),
  price: Type.Number(),
  room: Type.String(),
})
export type MovieScheduleBodyType = Static<typeof MovieScheduleBody>
