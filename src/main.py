import asyncio
import uvicorn
import config
from src.core_logger import logger
from service import *
from src.service.bot_http_cover.tasks import *

if __name__ == "__main__":
    logger.info("Bot HTTP cover started...")
    asyncio.create_task(uvicorn.run(app=app, host=config.SERVICE_HOST, port=config.SERVICE_PORT))