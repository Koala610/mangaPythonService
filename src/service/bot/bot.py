import aiogram
import src.config as config

from aiogram.contrib.fsm_storage.memory import MemoryStorage

telegram_bot = aiogram.Bot(token=config.API_TOKEN)
dp = aiogram.Dispatcher(telegram_bot, storage=MemoryStorage())

