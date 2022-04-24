import { Static, Type } from "@sinclair/typebox"

export enum Genre {
  Action,
  Adventure,
  Animation,
  Comedy,
  Drama,
  Fantasy,
  Historical,
  Horror,
  Romance,
  SciFi,
  Thriller,
  Western,
}

export const Movie = Type.Object({
  movie_id: Type.Integer(),
  title: Type.String(),
  duration: Type.Integer(),
  release_date: Type.String(),
  director: Type.String(),
  synopsys: Type.String(),
  genre: Type.Enum(Genre),
})

export type MovieType = Static<typeof Movie>
