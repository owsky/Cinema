import { Type, Static } from "@sinclair/typebox"

export const MoviePostBody = Type.Object({
  Title: Type.String(),
  Year: Type.String(),
  Runtime: Type.String(),
  Genre: Type.String(),
  Director: Type.String(),
  Plot: Type.String(),
  Actors: Type.Array(Type.String()),
})
export type MoviePostBodyType = Static<typeof MoviePostBody>
