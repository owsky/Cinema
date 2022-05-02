import { Static, Type } from "@sinclair/typebox"

export const MovieParams = Type.Object({
  movieId: Type.Number(),
})
export type MovieParamsType = Static<typeof MovieParams>
