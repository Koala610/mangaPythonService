from aiogram import types
from src.service.bot.bot import telegram_bot, dp
from ..models.user import create_user, subscribe_on_updates
from ..views.menu_markups import get_menu_markup
from ..views.users import get_config_menu_markup


@dp.message_handler(commands = ['start'])
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    create_user(user_id, message.from_user.first_name)
    await telegram_bot.send_message(user_id, "Hi!", reply_markup=get_menu_markup(user_id))

@dp.message_handler(
    lambda message: message.text and
    (message.text == '/subscribe' or message.text ==
     '🔊 Подписаться на обновления' or message.text == '🔇 Отписаться от обновлений')
)
async def subscribe(message: types.Message):
    user_id = message.from_user.id 
    subscribe_on_updates(user_id)
    mark_up = get_config_menu_markup(user_id)
    await telegram_bot.send_message(user_id, "Успешно", reply_markup=mark_up)
