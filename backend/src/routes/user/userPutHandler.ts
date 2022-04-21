import config from "../../config/setupEnvinronment"
import postgres from "../../db"
import createPassword from "../../utils/createPassword"
import generateSalt from "../../utils/generateSalt"

const userPutHandler = async (
  email: string,
  fullName: string,
  plainText: string
) => {
  const salt = await generateSalt()
  if (salt) {
    const password = await createPassword(plainText, salt, config.SECRET)
    if (password) {
      await postgres.usersMethods.createUser(email, fullName, password, salt)
    } else {
      throw new Error("Couldn't generate password")
    }
  } else {
    throw new Error("Couldn't generate salt")
  }
}
export default userPutHandler
