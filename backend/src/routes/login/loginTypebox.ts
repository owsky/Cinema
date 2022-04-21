import { Type, Static } from "@sinclair/typebox"

export const Login = Type.Object({
  email: Type.String(),
  password: Type.String(),
})
export type LoginType = Static<typeof Login>
