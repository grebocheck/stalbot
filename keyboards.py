from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from language import texts

# Клавіатура меню
menu_markup = {"EN": ReplyKeyboardMarkup(resize_keyboard=True, selective=True),
               "RU": ReplyKeyboardMarkup(resize_keyboard=True, selective=True)}
# EN меню
menu_markup["EN"].add(texts.get_history_price["EN"], texts.get_check_price["EN"])
menu_markup["EN"].add(texts.about_us_btn["EN"], texts.notif_emiss["EN"])
menu_markup["EN"].add(texts.update_language["EN"], texts.update_server["EN"])
# RU меню
menu_markup["RU"].add(texts.get_history_price["RU"], texts.get_check_price["RU"])
menu_markup["RU"].add(texts.about_us_btn["RU"], texts.notif_emiss["RU"])
menu_markup["RU"].add(texts.update_language["RU"], texts.update_server["RU"])

# Прибрати клавіатуру
remove_mark = ReplyKeyboardRemove()

# Клавіатура мов
lang_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
lang_markup.add(texts.en_lang_btn, texts.ru_lang_btn)

# Клавіатура серверів
server_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
server_markup.add(texts.eu_server_btn, texts.ru_server_btn)
server_markup.add(texts.na_server_btn, texts.sea_server_btn)

# Клавіатура скасування дії
cancel_markup = {"EN": ReplyKeyboardMarkup(resize_keyboard=True, selective=True),
                 "RU": ReplyKeyboardMarkup(resize_keyboard=True, selective=True)}
cancel_markup["EN"].add(texts.cancel_btn["EN"])
cancel_markup["RU"].add(texts.cancel_btn["RU"])