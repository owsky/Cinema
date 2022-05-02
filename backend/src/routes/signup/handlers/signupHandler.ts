import postgres from "../../../db"

const signupHandler = async (
  createPassword: (
    plaintextPassword: string,
    salt?: string | undefined
  ) => Promise<{ password: string; salt: string } | null>,
  email: string,
  fullName: string,
  plainTextPassword: string
) => {
  console.log(plainTextPassword)
  const passwordSalt = await createPassword(plainTextPassword)
  if (passwordSalt) {
    await postgres.usersMethods.createUser(
      email,
      fullName,
      passwordSalt.password,
      passwordSalt.salt
    )
  } else {
    throw new Error("Couldn't generate password")
  }
}
export default signupHandler
