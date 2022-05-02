import { Type, Static } from "@sinclair/typebox"

export const ActorQuery = Type.Object({
  actor_id: Type.Number(),
})
export type ActorQueryType = Static<typeof ActorQuery>
