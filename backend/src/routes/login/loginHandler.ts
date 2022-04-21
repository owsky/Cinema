import config from "../../config/setupEnvinronment"
import postgres from "../../db"
import createPassword from "../../utils/createPassword"
import signToken from "../../utils/signToken"

export default async function loginHandler(email: string, plainText: string) {
  const user = await postgres.usersMethods.getUser(email)
  if (user) {
    const salt = user.salt
    const verify = await createPassword(plainText, salt, config.SECRET)
    if (verify) {
      if (user.password === verify) {
        return signToken(email, user.full_name, user.user_role)
      }
    } else {
      throw new Error("Couldn't generate password")
    }
  }
}
