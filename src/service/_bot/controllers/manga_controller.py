import src.service._bot.models.bookmarks as bookmark_actions
import datetime

from aiogram import types

from src.service._bot.bot import telegram_bot, dp
from src import logger

from ..views.bookmarks import create_bookmark_response


@dp.message_handler(
    lambda message: message.text and
    (message.text == '/bookmarks' or message.text == '🔖 Вывести закладки')
)
async def get_bookmarks(message: types.Message):
    user_id = message.from_user.id
    storage_data = await dp.storage.get_data(user=user_id)
    bookmarks, is_renewed = await bookmark_actions.get_bookmarks(user_id, storage_data=storage_data)
    if is_renewed:
        storage_data = {
            "timestamp": datetime.datetime.now(),
            "bookmarks": bookmarks
        }
        logger.info("Made request")
        await dp.storage.set_data(user=user_id, data=storage_data)
    if bookmarks is None:
        await telegram_bot.send_message(user_id, "Ошибка при получении закладок. Попробуйте снова ввести свои данные через /account")
        return
    for bookmark in bookmarks:
        text, markup = create_bookmark_response(bookmark)
        await telegram_bot.send_message(user_id, text, reply_markup=markup)
