import postgres from "../../../db"

export default async function purchaseHistoryHandler(email: string) {
  const history = await postgres.usersMethods.getPurchaseHistory(email)
  return history
}
