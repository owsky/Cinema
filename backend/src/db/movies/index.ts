import getCurrentSchedule from "./getCurrentSchedule"
import getMovie from "./getMovie"
import getMovieSchedule from "./getMovieSchedule"
import insertNewMovie from "./insertNewMovie"
import addToSchedule from "./addToSchedule"
import removeFromSchedule from "./removeFromSchedule"
import editMovieSchedule from "./editMovieSchedule"
import removeMovie from "./removeMovie"

const moviesMethods = {
  getCurrentSchedule,
  getMovie,
  getMovieSchedule,
  insertNewMovie,
  removeMovie,
  addToSchedule,
  editMovieSchedule,
  removeFromSchedule,
}
export default moviesMethods
