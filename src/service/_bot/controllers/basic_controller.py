import aiogram
import src.logger
from src.service._bot.bot import telegram_bot, dp

@dp.message_handler(commands = ['start'])
async def handle_start(message: aiogram.types.Message):
    logger.info("Message recieved")
    await telegram_bot.send_message(message.from_user.id, "Hi!")
