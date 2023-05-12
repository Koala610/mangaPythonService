import src.service.bot as bot
import asyncio
import src.service.bot_http_cover as bot_controller

from src import logger
from src.entity import RMManga
from src.repository import user_repository
from src.service import rm_service
from src.config import UPDATE_FREQUENCY
from datetime import datetime, timedelta

@bot_controller.app.on_event("startup")
async def start_bot():
    logger.info("Bot started...")
    asyncio.create_task(bot.dp.start_polling())

# @bot_controller.app.on_event("startup")
def wrapper():
    async def send_updates():
        while True:
            data = await bot.dp.storage.get_data(user=-1)
            if data.get("last_updated") is None:
                await bot.dp.storage.set_data(user=-1, data={
                    "last_updated": datetime.now()
                })
                continue
            if datetime.now() - data.get("last_updated") > timedelta(minutes=UPDATE_FREQUENCY):
                logger.info("Checking updates...")
                await bot.dp.storage.update_data(user=-1, data={
                    "last_updated": datetime.now()
                })
                users = user_repository.find_by_subscription(is_subscribed=True)
                for user in users:
                    bookmarks = await rm_service.rm_service.get_bookmarks(user.user_id)
                    h = RMManga.hash_from_list(bookmarks)
                    if h != user.bookmarks_hash:
                        user_repository.update(user.user_id, bookmarks_hash=h)
                        await bot.telegram_bot.send_message(user.user_id, "Что-то изменилось у вас в закладках...")
            await asyncio.sleep(1)
    asyncio.create_task(send_updates())
