import asyncio
import uvicorn
import src.logger as logger

from config import SERVICE_PORT, SERVICE_HOST
from src.service import app


if __name__ == "__main__":
    logger.logger.info("Notification service started...")
    asyncio.create_task(uvicorn.run(app=app, host=SERVICE_HOST, port=SERVICE_PORT))