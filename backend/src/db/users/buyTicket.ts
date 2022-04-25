import { pool } from ".."
import logger from "../../logger"

export default async function buyTicket(
  userEmail: string,
  projectionId: number,
  seatCode: number
) {
  const client = await pool.connect()

  try {
    await client.query("BEGIN")

    interface RoomName {
      room: string
    }
    interface RoomNameQuery {
      rows: RoomName[]
    }

    const { rows: rooms }: RoomNameQuery = await client.query(
      `
        SELECT room
        FROM projections
        WHERE projection_id = $1
      `,
      [projectionId]
    )
    const room = rooms.at(0)?.room

    interface SeatId {
      seat_id: number
    }

    interface SeatIdQuery {
      rows: SeatId[]
    }

    const { rows: seats }: SeatIdQuery = await client.query(
      `
        SELECT seat_id
        FROM seats
        WHERE room = $1 AND code = $2
      `,
      [room, seatCode]
    )

    await client.query(
      `
        INSERT INTO tickets(user_email, projection, seat)
        VALUES($1, $2, $3);
      `,
      [userEmail, projectionId, seats.at(0)?.seat_id]
    )
    await client.query("COMMIT")
    return true
  } catch (e) {
    logger.error(e)
    await client.query("ROLLBACK")
    return false
  } finally {
    client.release()
  }
}
