import * as argon2 from "argon2"

export default async function verifyPassword(
  hash: string,
  plainText: string,
  salt: string,
  secret: string
): Promise<boolean> {
  try {
    return await argon2.verify(hash, plainText, {
      salt: Buffer.from(salt),
      secret: Buffer.from(secret),
    })
  } catch (e) {
    console.error(e)
    return false
  }
}
