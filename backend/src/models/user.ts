enum Role {
  user,
  admin,
}

export default interface User {
  email: string
  full_name: string
  password: string
  user_role: Role
}
