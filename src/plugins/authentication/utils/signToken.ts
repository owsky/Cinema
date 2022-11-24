import * as jwt from "jsonwebtoken"

export default function signToken(
  email: string,
  full_name: string,
  user_role: string,
  secret: string
) {
  const rawToken = jwt.sign({ email, full_name, user_role }, secret, {
    algorithm: "HS384",
    expiresIn: "7d",
  })
  return `Bearer ${rawToken}`
}
