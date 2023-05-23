import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiohttp.client_exceptions import ClientConnectionError
from src.core_logger import logger
from src.service._bot.bot import telegram_bot, dp
from src.service.support_service import support_service
from src.repository import user_repository
from src.config import MESSAGES_LIMIT
from ..views.menu_markups import get_menu_markup, support_menu
from ..utils.states import SendMessageStates, AnswerMessageStates
from ..models.support import answer_message

def check_if_user_support(fun):
    async def wrapper(message: types.Message):
        user_id = message.from_user.id
        if user_repository.check_if_support(user_id):
            await fun(message)
        else:
            await telegram_bot.send_message(user_id, "Недостаточно прав")
    return wrapper

@dp.message_handler(lambda message: message.text and
                    (message.text == '/message' or message.text == "📞 Отправить сообщение в поддержку"))
async def prepare_to_send_support_message(message: types.Message):
    await message.answer('Введите запрос в поддержку:')
    await SendMessageStates.in_process.set()

@dp.message_handler(state=SendMessageStates.in_process)
async def add_password(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '') == '/exit':
        await message.answer('Отменено!')
    else:
        user_id = message.from_user.id
        support_message = message.text
        try: 
            await support_service.create_support_message(user_id, support_message)
            await telegram_bot.send_message(user_id, 'Успешно!', reply_markup=get_menu_markup(user_id))
            logger.info(f"User {user_id} support message successfully sended")
        except ClientConnectionError:
            await telegram_bot.send_message(user_id, 'Упс! Внутрення ошибка. Повторите позже', reply_markup=get_menu_markup(user_id))
            logger.error(f"User {user_id} support ")
    await state.finish()


@dp.message_handler(
    lambda message: message.text and
    (message.text == '/support' or message.text ==
     '⌨️ Меню поддержки')
)
async def subscribe(message: types.Message):
    user_id = message.from_user.id 
    await telegram_bot.send_message(user_id, "Успешно", reply_markup=support_menu)

@dp.message_handler(
    lambda message: message.text and
    (message.text == '/support_messages' or message.text ==
     '✉️ Все сообщения')
)
@check_if_user_support
async def get_all_messages(message: types.Message):
    user_id = message.from_user.id 
    messages = await support_service.get_unprocessed_message() 
    if len(messages) == 0:
        await telegram_bot.send_message(user_id, "Пусто")
        return
    for i in messages:
        message_markup = types.InlineKeyboardMarkup()
        result_message = f"""
            ID пользователя: {i.get("user_id")}
Сообщение: {i.get("message")}
        """
        if i.get("support_id") == None:
            message_markup.add(types.InlineKeyboardButton("Ответить", callback_data=f"answer::{i.get('id')}"))
        await telegram_bot.send_message(user_id, result_message, reply_markup=message_markup)

@dp.message_handler(
    lambda message: message.text and
    (message.text == '/support_processed_messages' or message.text ==
     '📩 Обработанные')
)
@check_if_user_support
async def get_processing_messages(message: types.Message):
    user_id = message.from_user.id 
    support_id = user_repository.find_user_support_id(user_id=user_id)
    messages: dict = await support_service.get_support_message(support_id, processed=1)
    if len(messages) == 0:
        await telegram_bot.send_message(user_id, "Пусто")
        return
    for i in messages:
        message_markup = types.InlineKeyboardMarkup()
        result_message = f"""
            ID пользователя: {i.get("user_id")}
Сообщение: {i.get("message")}
        """
        if i.get("support_id") == None:
            message_markup.add(types.InlineKeyboardButton("Ответить", callback_data=f"answer::{i.get('id')}"))
        await telegram_bot.send_message(user_id, result_message, reply_markup=message_markup)

@dp.callback_query_handler(lambda c: 'answer' in c.data)
async def process_callback_details_btn(callback_query: types.CallbackQuery):
    await telegram_bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    callback_data = callback_query.data.split("::")
    message_id = callback_data[1]
    storage_data = await dp.storage.get_data(user=user_id)
    storage_data["message_id"] = message_id
    await dp.storage.set_data(user=user_id, data = storage_data)
    await telegram_bot.send_message(user_id, "Введите ответ на сообщение:")
    await AnswerMessageStates.in_process.set()

@dp.message_handler(state=AnswerMessageStates.in_process)
async def add_password(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '') == '/exit':
        await message.answer('Отменено!')
    else:
        user_id = message.from_user.id
        response = message.text
        storage_data = await dp.storage.get_data(user=user_id)
        message_id = storage_data.get("message_id")
        support_id = user_repository.find_user_support_id(user_id)
        del storage_data["message_id"]
        await dp.storage.set_data(user=user_id, data=storage_data)

        await answer_message(message_id, user_id, response)
        await telegram_bot.send_message(user_id, "Отправлено")
#         message_to_response = await support_service.get_message(message_id)
#         support_id = user_repository.find_user_support_id(user_id)
#         await support_service.set_message_response(message_id=message_id, response=response, support_id=support_id)
#         final_message = f"""
#             Вам ответили
# Сообщение: {message_to_response.get("message")}
# ID члена поддержки: {support_id}
# Ответ: {response}
#         """
#         await telegram_bot.send_message(user_id, "Отправлено")
#         await telegram_bot.send_message(message_to_response.get("user_id"), final_message)
    await state.finish()