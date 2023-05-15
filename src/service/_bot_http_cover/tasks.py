import src.service.bot as bot
import asyncio
import src.service.bot_http_cover as bot_controller

from src import logger

@bot_controller.app.on_event("startup")
async def start_bot():
    logger.info("Bot started...")
    asyncio.create_task(bot.dp.start_polling())