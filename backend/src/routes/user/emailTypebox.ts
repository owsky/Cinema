import { Type, Static } from "@sinclair/typebox"

export const Email = Type.Object({
  email: Type.String({ format: "email" }),
})
export type EmailType = Static<typeof Email>
