import * as argon2 from "argon2"
import generateSalt from "./generateSalt"

export default async function createPassword(
  plainText: string,
  secret: string,
  salt?: string
): Promise<{ password: string; salt: string } | null> {
  try {
    let userSalt: string | null
    if (!salt) userSalt = await generateSalt()
    else userSalt = salt
    if (userSalt) {
      const hash = await argon2.hash(plainText, {
        salt: Buffer.from(userSalt),
        secret: Buffer.from(secret),
      })
      return {
        password: hash,
        salt: userSalt,
      }
    } else {
      throw new Error("Couldn't generate the salt")
    }
  } catch (e) {
    console.error(e)
    return null
  }
}
