import { Type, Static } from "@sinclair/typebox"
import { SuccessResponse } from "../SuccessTypebox"

export const LoginRequest = Type.Object({
  email: Type.String(),
  password: Type.String(),
})
export type LoginRequestType = Static<typeof LoginRequest>

const Token = Type.Object({ token: Type.String() })
export const LoginResponse = Type.Intersect([SuccessResponse, Token])
