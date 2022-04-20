import * as argon2 from "argon2"

export default async function createPassword(
  plainText: string,
  salt: string,
  secret: string
): Promise<string | null> {
  try {
    const hash = await argon2.hash(plainText, {
      salt: Buffer.from(salt),
      secret: Buffer.from(secret),
    })
    return hash
  } catch (e) {
    console.error(e)
    return null
  }
}
