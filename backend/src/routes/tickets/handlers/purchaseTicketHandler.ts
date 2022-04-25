import postgres from "../../../db"
import logger from "../../../logger"

export default async function purchaseTicketHandler(
  userEmail: string,
  projectionId: number,
  seatCode: number
) {
  try {
    return await postgres.usersMethods.buyTicket(
      userEmail,
      projectionId,
      seatCode
    )
  } catch (e) {
    logger.error(e)
    return false
  }
}
