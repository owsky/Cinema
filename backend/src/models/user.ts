import { Static, Type } from "@sinclair/typebox"

export enum Role {
  user = "user",
  admin = "admin",
}

export const User = Type.Object({
  email: Type.String(),
  full_name: Type.String(),
  password: Type.String(),
  salt: Type.String(),
  user_role: Type.Enum(Role),
})

export type UserType = Static<typeof User>
