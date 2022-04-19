type Seat = {
  code: number
}

export default interface Room {
  roomId: number
  name: string
  seats: Seat[]
}
