import src.service._bot.models.bookmarks as bookmark_actions

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
    bookmarks = await bookmark_actions.get_bookmarks(user_id, limit=50, offset=0)
    if bookmarks is None:
        await telegram_bot.send_message(user_id, "Ошибка при получении закладок. Попробуйте снова ввести свои данные через /account")
        return
    for bookmark in bookmarks:
        text, markup = create_bookmark_response(bookmark)
        await telegram_bot.send_message(user_id, text, reply_markup=markup)


