from aiogram.dispatcher import FSMContext
from aiogram import types
from src.core_logger import logger
from src.service._bot.bot import telegram_bot, dp
from ..models.user import auth
from ..views.menu_markups import get_menu_markup
from ..views.users import get_config_menu_markup
from ..utils.states import AccStates


@dp.message_handler(lambda message: message.text and
                    (message.text == '/menu' or message.text == "📋 Меню"))
async def show_menu(message: types.Message):
    await telegram_bot.send_message(message.from_user.id, "Меню:", reply_markup=get_menu_markup(message.from_user.id))

@dp.message_handler(lambda message: message.text and
                    (message.text == '/settings' or message.text == "⚙️ Настройки"))
async def show_settings(message: types.Message):
    user_id = message.from_user.id
    mark_up = get_config_menu_markup(user_id)
    await telegram_bot.send_message(message.from_user.id, "Настройки:", reply_markup=mark_up)

@dp.message_handler(lambda message: message.text and
                    (message.text == '/account' or message.text == "📝 Изменить аккаунт"))
async def add_account(message: types.Message):
    await message.answer('Введите ваш логин или введите /exit для отмены')
    await AccStates.login.set()


@dp.message_handler(state=AccStates.login)
async def add_username(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '') == '/exit':
        await state.finish()
        await message.answer('Отменено!')
    else:
        user_id = message.from_user.id
        username = message.text
        await state.update_data(username=username)
        await telegram_bot.send_message(user_id, 'Введите ваш пароль или введите /exit для отмены')
        await AccStates.password.set()


@dp.message_handler(state=AccStates.password)
async def add_password(message: types.Message, state: FSMContext):
    if message.text.replace(' ', '') == '/exit':
        await message.answer('Отменено!')
    else:
        user_id = message.from_user.id
        password = message.text
        state_data = await state.get_data()
        username = state_data.get("username")
        data = {
            "username": username,
            "password": password
        }
        if await auth(user_id, data):
            await telegram_bot.send_message(user_id, 'Успешно!', reply_markup=get_menu_markup(user_id))
            logger.info(f"User {user_id} successfully authorized")
        else:
            await telegram_bot.send_message(user_id, 'Ошибка! Неверные данные', reply_markup=get_menu_markup(user_id))
            logger.error(f"User {user_id} didn't authorized")

    await state.finish()
