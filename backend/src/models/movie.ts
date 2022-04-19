enum Genre {
  Action,
  Adventure,
  Animation,
  Comedy,
  Drama,
  Fantasy,
  Historical,
  Horror,
  Romance,
  SciFi,
  Thriller,
  Western,
}

export default interface Movie {
  movieId: number
  title: string
  synopsys: string
  genre: Genre
}
