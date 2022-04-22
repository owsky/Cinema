import { Type, Static } from "@sinclair/typebox"

export const Signup = Type.Object({
  email: Type.String(),
  full_name: Type.String(),
  password: Type.String(),
  user_role: Type.Optional(Type.String()),
})
export type SignupType = Static<typeof Signup>
