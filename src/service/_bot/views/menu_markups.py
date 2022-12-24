import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

cng_acc_btn = KeyboardButton("📝 Изменить аккаунт")
unreads_btn = KeyboardButton("📒 Вывести недочитанные")
bookmarks_btn = KeyboardButton("🔖 Вывести закладки")
settings_btn = KeyboardButton("⚙️ Настройки")
menu_btn = KeyboardButton("📋 Меню")
subscribe_btn = '🔊 Подписаться на обновления'
unsubscribe_btn = '🔇 Отписаться от обновлений'


def create_reply_keyboard_markup(row_width=1):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=row_width
    )


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