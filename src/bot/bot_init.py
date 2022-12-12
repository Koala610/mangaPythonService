from config import *


storage = MemoryStorage()
telegram_bot = Bot(token=API_TOKEN)
dp = Dispatcher(telegram_bot, storage=storage)

