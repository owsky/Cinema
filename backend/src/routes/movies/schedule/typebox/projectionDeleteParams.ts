import { Static, Type } from "@sinclair/typebox"

export const ProjectionDeleteParams = Type.Object({
  projectionId: Type.Number(),
})
export type ProjectionDeleteParamsType = Static<typeof ProjectionDeleteParams>
