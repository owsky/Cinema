import * as crypto from "crypto"
import { promisify } from "util"

const promisifiedRandomBytes = promisify(crypto.randomBytes)

export default async function generateSalt(): Promise<string | null> {
  try {
    return (await promisifiedRandomBytes(16)).toString()
  } catch (e) {
    console.error(e)
    return null
  }
}
