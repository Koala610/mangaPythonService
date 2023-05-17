from aiogram import types
from aiogram.dispatcher import FSMContext
from aiohttp.client_exceptions import ClientConnectionError
from src.logger import logger
from src.service._bot.bot import telegram_bot, dp
from src.service.support_service import support_service
from ..views.menu_markups import get_menu_markup
from ..utils.states import SendMessageStates


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
