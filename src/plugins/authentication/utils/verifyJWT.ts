import * as jwt from "jsonwebtoken"

export default function verifyToken(token: string, secret: string) {
  const rawToken = token.split(" ").at(1)
  if (rawToken) {
    return jwt.verify(rawToken, secret, {
      algorithms: ["HS384"],
    })
  }
}
