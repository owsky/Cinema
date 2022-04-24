import { Type } from "@sinclair/typebox"

export const ErrorResponse = Type.Object({
  error: Type.String(),
  message: Type.Optional(Type.String()),
})
