import aiogram
from src.service._bot.bot import telegram_bot, dp
from src.repository import user_repository
from src import logger
from ..models.user import create_user
from ..views.menu_markups import main_menu


@dp.message_handler(commands = ['start'])
async def handle_start(message: aiogram.types.Message):
    user_id = message.from_user.id
    create_user(user_id, message.from_user.first_name)
    await telegram_bot.send_message(user_id, "Hi!", reply_markup=main_menu)
