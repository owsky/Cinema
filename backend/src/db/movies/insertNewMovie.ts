import { pool } from ".."

export default async function insertNewMovie(
  title: string,
  year: string,
  runtime: string,
  genre: string,
  director: string,
  plot: string,
  actors: string[]
) {
  await pool.query(
    `
    INSERT INTO movies(title, runtime, year, genre, actors, director, plot)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
  `,
    [title, runtime, year, genre, actors, director, plot]
  )
}
