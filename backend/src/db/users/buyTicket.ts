import { pool } from ".."
import logger from "../../logger"
import format from "pg-format"

interface RoomName {
  room: string
}
interface RoomNameQuery {
  rows: RoomName[]
}

interface SeatId {
  seat_id: number
}

interface SeatIdQuery {
  rows: SeatId[]
}

export default async function buyTicket(
  userEmail: string,
  projectionId: number,
  seatCodes: number[]
) {
  const client = await pool.connect()

  try {
    await client.query("BEGIN")

    const { rows: rooms }: RoomNameQuery = await client.query(
      `
        SELECT room
        FROM projections
        WHERE projection_id = $1
      `,
      [projectionId]
    )
    const room = rooms.at(0)?.room

    const { rows: seatIds }: SeatIdQuery = await client.query(
      `
        SELECT seat_id
        FROM seats
        WHERE room = $1 AND code = ANY($2)
      `,
      [room, seatCodes]
    )
    if (seatIds.length === 0) throw new Error("Invalid seats")

    const queryValues = seatIds.map(seat => {
      return [userEmail, projectionId, seat.seat_id]
    })

    await client.query(
      // eslint-disable-next-line @typescript-eslint/no-unsafe-call
      format(
        `INSERT INTO tickets(user_email, projection, seat) VALUES %L`,
        queryValues
      )
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
