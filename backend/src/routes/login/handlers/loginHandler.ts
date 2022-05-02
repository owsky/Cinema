import postgres from "../../../db"

export default async function loginHandler(
  createPassword: (
    plaintextPassword: string,
    salt?: string | undefined
  ) => Promise<{
    password: string
    salt: string
  } | null>,
  signToken: (email: string, fullName: string, userRole: string) => string,
  email: string,
  plainText: string
) {
  const user = await postgres.usersMethods.getUser(email)
  if (user) {
    const salt = user.salt
    const verify = await createPassword(plainText, salt)
    if (verify) {
      if (user.password === verify.password) {
        return signToken(user.email, user.full_name, user.user_role)
      }
    } else {
      throw new Error("Couldn't generate password")
    }
  }
}
