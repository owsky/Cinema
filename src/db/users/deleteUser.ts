import { pool } from ".."

export default async function deleteUser(email: string) {
  await pool.query(`DELETE FROM users WHERE email = $1`, [email])
}
