import { Static, Type } from "@sinclair/typebox"

export const MovieSchedulePostBody = Type.Object({
  movie_id: Type.Number(),
  start_date: Type.String(),
  price: Type.Number(),
  room: Type.String(),
})
export type MovieSchedulePostBodyType = Static<typeof MovieSchedulePostBody>
