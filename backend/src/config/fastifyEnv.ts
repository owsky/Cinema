import { FastifyInstance } from "fastify"
import fastifyEnv, { fastifyEnvOpt } from "fastify-env"

declare module "fastify" {
  interface FastifyInstance {
    config: {
      HOST: string
      PORT: string
      DB_HOST: string
      DB_PORT: string
      DB_USER: string
      DB_PASSWORD: string
      PEPPER: string
      SECRET: string
    }
  }
}

const schema = {
  type: "object",
  required: ["PORT", "HOST", "DB_PASSWORD", "PEPPER", "SECRET"],
  properties: {
    HOST: {
      type: "string",
      default: "127.0.0.1",
    },
    PORT: {
      type: "string",
      default: "3000",
    },
    DB_HOST: {
      type: "string",
      default: "127.0.0.1",
    },
    DB_PORT: {
      type: "string",
      default: "5432",
    },
    DB_USER: {
      type: "string",
      default: "postgres",
    },
    DB_PASSWORD: {
      type: "string",
    },
    PEPPER: {
      type: "string",
    },
    SECRET: {
      type: "string",
    },
  },
}

const options: fastifyEnvOpt = {
  confKey: "config",
  schema: schema,
  data: process.env,
  dotenv: true,
}

export default async function setupEnvironment(fastify: FastifyInstance) {
  fastify.register(fastifyEnv, options)
  await fastify.after()
}
