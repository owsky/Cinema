import * as jwt from "jsonwebtoken"
import config from "../config"

export default function signToken(
  email: string,
  full_name: string,
  user_role: string
) {
  const rawToken = jwt.sign({ email, full_name, user_role }, config.SECRET, {
    algorithm: "HS384",
    expiresIn: "7d",
  })
  return `Bearer ${rawToken}`
}
