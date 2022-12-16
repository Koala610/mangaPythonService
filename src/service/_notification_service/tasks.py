import src.service.bot as bot
import asyncio
import src.service.notification_service as notification_service
import src.logger as logger

@notification_service.app.on_event("startup")
async def start_bot():
    logger.logger.info("Bot started...")
    asyncio.create_task(bot.dp.start_polling())