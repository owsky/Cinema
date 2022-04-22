import dbConnect from "./config/dbConnect"
import config from "./config/setupEnvinronment"
import logger from "./logger"
import createServer from "./server"

async function start() {
  try {
    await dbConnect()
    const fastify = await createServer()
    await fastify.listen(config.PORT, config.HOST)
  } catch (e) {
    logger.error(e)
    process.exit(-1)
  }
}
void start()
