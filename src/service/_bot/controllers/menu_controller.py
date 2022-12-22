from aiogram.dispatcher import FSMContext
from aiogram import types
from src import logger
from src.service._bot.bot import telegram_bot, dp
from ..models.user import auth
from ..views.menu_markups import main_menu
from ..utils.states import AccStates

@dp.message_handler(lambda message: message.text and 
                    (message.text == '/account' or message.text =="📝 Изменить аккаунт"))
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
        await auth(user_id, data)
        await telegram_bot.send_message(user_id, 'Успешно!', reply_markup=main_menu)
        logger.info(f"User {user_id} successfully authorized")

    await state.finish()