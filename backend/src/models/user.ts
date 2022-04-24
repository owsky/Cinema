import { Static, Type } from "@sinclair/typebox"

export const User = Type.Object({
  email: Type.String(),
  full_name: Type.String(),
  password: Type.String(),
  salt: Type.String(),
  user_role: Type.String(),
})

export type UserType = Static<typeof User>
