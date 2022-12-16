import aiogram
import config 

telegram_bot = aiogram.Bot(token=config.API_TOKEN)
dp = aiogram.Dispatcher(telegram_bot)

