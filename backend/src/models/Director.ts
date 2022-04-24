import { Type, Static } from "@sinclair/typebox"

export const Director = Type.Object({
  director_id: Type.Number(),
  full_name: Type.String(),
})

export type DirectorType = Static<typeof Director>
