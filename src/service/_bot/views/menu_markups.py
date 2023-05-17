import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from ..models.user import check_if_support

cng_acc_btn = KeyboardButton("📝 Изменить аккаунт")
unreads_btn = KeyboardButton("📒 Вывести недочитанные")
bookmarks_btn = KeyboardButton("🔖 Вывести закладки")
settings_btn = KeyboardButton("⚙️ Настройки")

support_message_btn = KeyboardButton("📞 Отправить сообщение в поддержку")
support_menu_btn = KeyboardButton("⌨️ Меню поддержки")

all_support_message_btn = KeyboardButton("✉️ Все сообщения")
user_support_message_btn = KeyboardButton("📩 В обработке")

menu_btn = KeyboardButton("📋 Меню")

subscribe_btn = '🔊 Подписаться на обновления'
unsubscribe_btn = '🔇 Отписаться от обновлений'


def create_reply_keyboard_markup(row_width=1):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=row_width
    )

def create_default_main_menu_markup():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=1
    ).add(bookmarks_btn, unreads_btn, settings_btn, support_message_btn)

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=1
).add(bookmarks_btn, unreads_btn, settings_btn)

cng_acc_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=1
).add(cng_acc_btn, menu_btn)

settings_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=1
).add(cng_acc_btn, menu_btn)

support_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=1
).add(all_support_message_btn, user_support_message_btn, menu_btn)

def create_symbol_markup(keys):
    markup = create_reply_keyboard_markup(row_width=len(keys)//5)
    d = get_symbol_dict()
    for i in keys:
        markup.add(d[i])
    return markup

def get_symbol_dict():
    res = None
    with open("./src/resources/alphabet.json", "r") as f:
        res = json.loads(f.read()) 
    return res

def get_menu_markup(user_id: int):
    menu = create_default_main_menu_markup()
    if check_if_support(user_id=user_id):
        menu.add(support_menu_btn)
    return menu
