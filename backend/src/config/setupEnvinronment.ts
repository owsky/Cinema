import * as dotenv from "dotenv"

interface EnvI {
  HOST: string | undefined
  PORT: string | undefined
  SECRET: string | undefined
  PGHOST: string | undefined
  PGPORT: string | undefined
  PGDATABASE: string | undefined
  PGUSER: string | undefined
  PGPASSWORD: string | undefined
}

interface Config {
  HOST: string
  PORT: string
  SECRET: string
  PGHOST: string
  PGPORT: string
  PGDATABASE: string
  PGUSER: string
  PGPASSWORD: string
}

function setupEnvironment(): Config {
  const env = dotenv.config()
  if (env.error) throw env.error

  const envVariables: EnvI = {
    HOST: process.env.HOST,
    PORT: process.env.PORT,
    SECRET: process.env.SECRET,
    PGHOST: process.env.PGHOST,
    PGPORT: process.env.PGPORT,
    PGDATABASE: process.env.PGDATABASE,
    PGUSER: process.env.PGUSER,
    PGPASSWORD: process.env.PGPASSWORD,
  }

  for (const [key, value] of Object.entries(envVariables)) {
    if (value === undefined) throw new Error(`Missing key ${key} in config.env`)
  }

  return envVariables as Config
}

const config = setupEnvironment()
export default config
