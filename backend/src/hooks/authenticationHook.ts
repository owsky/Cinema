import verifyToken from "../utils/verifyToken"

function authenticationHook(token: string | undefined) {
  if (token && verifyToken(token)) return true
  return false
}
export default authenticationHook
