import postgres from "../../../db"
import logger from "../../../logger"

export default async function purchaseTicketHandler(
  userEmail: string,
  projectionId: number,
  seatCodes: number[]
) {
  try {
    return await postgres.usersMethods.buyTicket(
      userEmail,
      projectionId,
      seatCodes
    )
  } catch (e) {
    logger.error(e)
    return false
  }
}
