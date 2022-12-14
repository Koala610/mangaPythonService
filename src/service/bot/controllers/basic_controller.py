import aiogram
from ...bot import telegram_bot, dp

@dp.message_handler(commands = ['start'])
async def handle_start(message: aiogram.types.Message):
    print(message.from_user.id)
    await telegram_bot.send_message(message.from_user.id, "Hi!")
