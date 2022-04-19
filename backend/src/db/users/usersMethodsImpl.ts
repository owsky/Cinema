import IUsersMethods from "./IUsersMethods"
import getUser from "./methods/getUser"
import createUser from "./methods/createUser"

const usersMethodsImpl: IUsersMethods = {
  getUser,
  createUser,
}
export default usersMethodsImpl
