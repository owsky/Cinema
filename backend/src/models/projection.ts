import { Static, Type } from "@sinclair/typebox"

export const Projection = Type.Object({
  projection_id: Type.Integer(),
  room: Type.String(),
  start_date: Type.String(),
  end_date: Type.String(),
  price: Type.String(),
  title: Type.String(),
  duration: Type.String(),
  release_date: Type.String(),
  synopsys: Type.String(),
  genre: Type.String(),
  director: Type.String(),
})

export type ProjectionType = Static<typeof Projection>
