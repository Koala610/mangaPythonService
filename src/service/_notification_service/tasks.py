import src.service.bot as bot
import asyncio
import src.service.notification_service as notification_service

@notification_service.app.on_event("startup")
async def start_bot():
    asyncio.create_task(bot.dp.start_polling())