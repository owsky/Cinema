import Movie from "./movie"
import Room from "./room"

export default interface Projection {
  projectionId: number
  movie: Movie
  room: Room
  startDate: Date
  endDate: Date
}
