import src.service._bot.models.bookmarks as bookmark_actions
import datetime
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from src.service._bot.bot import telegram_bot, dp
from src.logger import logger

from ..views.bookmarks import create_bookmark_response, create_unread_response
from ..utils.states import BookmarkShowingStates
from ..views.menu_markups import create_symbol_markup, get_menu_markup


@dp.message_handler(
    lambda message: message.text and
    (message.text == '/unreads' or message.text == '📒 Вывести недочитанные')
)
async def get_bookmarks(message: types.Message):
    user_id = message.from_user.id
    bookmarks = await bookmark_actions.get_bookmarks(user_id, dp)
    if bookmarks is None:
        await telegram_bot.send_message(user_id, "Ошибка при получении. Попробуйте снова ввести свои данные через /account")
        return
    for bookmark in bookmarks:
        if bookmark.unread_chapters < 1 or bookmark.current_chapter.volume == -1:
            continue
        text, markup = create_unread_response(bookmark)
        await telegram_bot.send_message(user_id, text, reply_markup=markup)
        await asyncio.sleep(0.1)


@dp.message_handler(
    lambda message: message.text and
    (message.text == '/bookmarks' or message.text == '🔖 Вывести закладки')
)
async def get_bookmarks(message: types.Message):
    user_id = message.from_user.id
    logger.info("123")
    bookmarks = await bookmark_actions.get_bookmarks(user_id, dp, return_dict=True)
    if bookmarks is None:
        await telegram_bot.send_message(user_id, "Ошибка при получении. Попробуйте снова ввести свои данные через /account")
    markup = create_symbol_markup(bookmarks.keys())
    await telegram_bot.send_message(message.from_user.id, "Закладки:", reply_markup=markup)
    await telegram_bot.send_message(message.from_user.id, "Введите /exit для выхода")
    await BookmarkShowingStates.in_process.set()


@dp.message_handler(state=BookmarkShowingStates.in_process)
async def add_username(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.replace(' ', '') == '/exit':
        await state.finish()
        await telegram_bot.send_message(message.from_user.id, "Успешно...", reply_markup=get_menu_markup(user_id))
    else:
        letter = message.text.split(" ")
        if len(letter) != 2:
            await telegram_bot.send_message(message.from_user.id, "Неверный вариант...")
            return
        letter = letter[1]
        bookmarks = await bookmark_actions.get_bookmarks(user_id, dp, return_dict=True)
        markup = create_symbol_markup(bookmarks.keys())
        bookmarks = bookmarks[letter]
        for bookmark in bookmarks:
            text, mark_up = create_bookmark_response(bookmark)
            await telegram_bot.send_message(user_id, text, reply_markup=mark_up)
        await telegram_bot.send_message(message.from_user.id, "Закладки:", reply_markup=markup)
        await telegram_bot.send_message(message.from_user.id, "Введите /exit для выхода")
