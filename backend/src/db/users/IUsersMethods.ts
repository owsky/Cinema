import User from "../../models/user"

export default interface IUsersMethods {
  getUser(email: string): Promise<User | null>
  createUser(
    email: string,
    fullName: string,
    password: string,
    salt: string
  ): Promise<void>
}
