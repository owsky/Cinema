import { PostgresDb } from "fastify-postgres"
import User from "../../models/user"

export default interface IUsersMethods {
  getUser(
    db: PostgresDb & Record<string, PostgresDb>,
    email: string
  ): Promise<User | null>
  createUser(
    db: PostgresDb & Record<string, PostgresDb>,
    email: string,
    fullName: string,
    password: string,
    salt: string
  ): Promise<void>
}
