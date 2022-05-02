import { Type, Static } from "@sinclair/typebox"

export const ScheduleQuery = Type.Object({
  currentWeek: Type.Optional(Type.Boolean()),
})
export type ScheduleQueryType = Static<typeof ScheduleQuery>
