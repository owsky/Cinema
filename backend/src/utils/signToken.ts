import * as jwt from "jsonwebtoken"
import config from "../config"

export default function signToken(
  email: string,
  full_name: string,
  user_role: string
) {
  return jwt.sign({ email, full_name, user_role }, config.SECRET, {
    algorithm: "HS256",
  })
}
