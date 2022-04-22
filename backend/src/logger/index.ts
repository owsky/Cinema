import config from "../config"
import pino from "pino"

const logger = pino(
  config.CONTEXT !== "production"
    ? {
        transport: {
          target: "pino-pretty",
          options: {
            colorize: true,
          },
        },
      }
    : {}
)
export default logger
