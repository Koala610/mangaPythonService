import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *


storage = MemoryStorage()
telegram_bot = Bot(token=API_TOKEN)
dp = Dispatcher(telegram_bot, storage=storage)

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, skip_updates=True, loop=loop)