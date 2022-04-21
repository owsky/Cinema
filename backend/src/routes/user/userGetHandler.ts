import postgres from "../../db/index"

const userGetHandler = async (email: string) => {
  const user = await postgres.usersMethods.getUser(email)
  return user
}
export default userGetHandler
