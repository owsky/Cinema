import { Static, Type } from "@sinclair/typebox"

export const Actor = Type.Object({
  actor_id: Type.Number(),
  full_name: Type.String(),
  starring: Type.Array(Type.String()),
})

export type ActorType = Static<typeof Actor>
