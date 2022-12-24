import asyncio
import uvicorn
import config
import logger

from service import app

if __name__ == "__main__":
    logger.logger.info("Bot controller started...")
    asyncio.create_task(uvicorn.run(app=app, host=config.SERVICE_HOST, port=config.SERVICE_PORT))