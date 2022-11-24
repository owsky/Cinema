import { Static, Type } from "@sinclair/typebox"

export const Movie = Type.Object({
  movie_id: Type.Integer(),
  title: Type.String(),
  runtime: Type.Integer(),
  year: Type.Integer(),
  director: Type.String(),
  plot: Type.String(),
  genre: Type.String(),
})

export type MovieType = Static<typeof Movie>
