import * as jwt from "jsonwebtoken"
import config from "../config"

export default function verifyToken(token: string) {
  const rawToken = token.split(" ").at(1)
  if (rawToken) {
    return jwt.verify(rawToken, config.SECRET, {
      algorithms: ["HS384"],
    })
  }
}
