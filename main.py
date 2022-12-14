import asyncio
import uvicorn
from config import SERVICE_PORT, SERVICE_HOST
from src.service import app


if __name__ == "__main__":
    asyncio.create_task(uvicorn.run(app=app, host=SERVICE_HOST, port=SERVICE_PORT))