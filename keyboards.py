from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from bot import lng

# Клавиатура смены языка:
kbLang = InlineKeyboardMarkup()
kbLangwrd = 'lng:'
kbLang.add(
    InlineKeyboardButton('русский 🇷🇺', callback_data=f'{kbLangwrd}ru'),
    InlineKeyboardButton('українська 🇺🇦', callback_data=f'{kbLangwrd}uk'),
    InlineKeyboardButton('english 🇬🇧', callback_data=f'{kbLangwrd}en'),
)


async def get_main_keyboard(user):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton(await lng.trans('История цен 📈', user)),
        KeyboardButton(await lng.trans('Проверить цену💰', user))
    )

    kb.add(
        KeyboardButton(await lng.trans('Сменить настройки ⚙️', user)),
    )
    return kb


# regions = await scb.get_regions()
regions = [
    {'id': 'RU', 'name': 'RUSSIA'},
    {'id': 'EU', 'name': 'EUROPE'},
    {'id': 'NA', 'name': 'NORTH AMERICA'},
    {'id': 'SEA', 'name': 'SOUTH EAST ASIA'}
]


async def get_regions_keyboard():
    kb = InlineKeyboardMarkup(resize_keyboard=True)

    kbRgnwrd = 'rgn:'
    for region in regions:
        kb.add(
            InlineKeyboardButton(region['name'], callback_data=f'{kbRgnwrd}{region["id"]}'),
        )
    return kb


async def get_cancel_keyboard(user):
    kb = InlineKeyboardMarkup(resize_keyboard=True)

    kb.add(InlineKeyboardButton(await lng.trans('Отмена❌', user), callback_data="cancel"))
    return kb


async def get_emission_keyboard(user):
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kbRgnwrd = 'emi:'
    kb.add(
        InlineKeyboardButton(await lng.trans('Включить✅', user),
                             callback_data=f'{kbRgnwrd}1'),
        InlineKeyboardButton(await lng.trans('Отключить❌', user),
                             callback_data=f'{kbRgnwrd}0')
    )
    return kb


async def get_emission_close_keyboard(user):
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kbRgnwrd = 'emic'
    kb.add(
        InlineKeyboardButton(await lng.trans('Отключить уведомления❌', user),
                             callback_data=f'{kbRgnwrd}0')
    )
    return kb


async def get_cur_price_keyboard(user, next_btn: bool, back_btn: bool, order: bool,
                                 page: int, item: str, select: str):
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kbRgnwrd = 'cur:'
    btns = []
    btns_foot = []
    if order:
        order_call = 1
    else:
        order_call = 0
    if back_btn:
        button_back = InlineKeyboardButton("◀️",
                                           callback_data=f'{kbRgnwrd}back:{page}:{item}:{select}:{order_call}')
        btns.append(button_back)
    if next_btn:
        button_next = InlineKeyboardButton("▶️",
                                           callback_data=f'{kbRgnwrd}next:{page}:{item}:{select}:{order_call}')
        btns.append(button_next)

    buyout_name = await lng.trans("Выкуп", user)
    time_name = await lng.trans("Время", user)
    bid_name = await lng.trans("Ставка", user)
    if order:
        pris = "🔼"
    else:
        pris = "🔽"
    if select == "buyout_price":
        buyout_name += pris
    elif select == "time_left":
        time_name += pris
    elif select == "current_price":
        bid_name += pris

    btns_foot.append(InlineKeyboardButton(buyout_name,
                                          callback_data=f'{kbRgnwrd}buyout_price:{page}:{item}:{select}:{order_call}'))
    btns_foot.append(InlineKeyboardButton(time_name,
                                          callback_data=f'{kbRgnwrd}time_left:{page}:{item}:{select}:{order_call}'))
    btns_foot.append(InlineKeyboardButton(bid_name,
                                          callback_data=f'{kbRgnwrd}current_price:{page}:{item}:{select}:{order_call}'))

    if btns:
        kb.add(*btns)
        kb.add(*btns_foot)
        return kb
    else:
        return None


remove_keyboard = ReplyKeyboardRemove()

# Клавіатура меню
# menu_markup = {"EN": ReplyKeyboardMarkup(resize_keyboard=True, selective=True),
#                "RU": ReplyKeyboardMarkup(resize_keyboard=True, selective=True)}
# # EN меню
# menu_markup["EN"].add(texts.get_history_price["EN"], texts.get_check_price["EN"])
# menu_markup["EN"].add(texts.about_us_btn["EN"], texts.notif_emiss["EN"])
# menu_markup["EN"].add(texts.update_language["EN"], texts.update_server["EN"])
# # RU меню
# menu_markup["RU"].add(texts.get_history_price["RU"], texts.get_check_price["RU"])
# menu_markup["RU"].add(texts.about_us_btn["RU"], texts.notif_emiss["RU"])
# menu_markup["RU"].add(texts.update_language["RU"], texts.update_server["RU"])

# # Прибрати клавіатуру
# remove_mark = ReplyKeyboardRemove()

# # Клавіатура мов
# lang_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
# lang_markup.add(texts.en_lang_btn, texts.ru_lang_btn)

# # Клавіатура серверів
# server_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
# server_markup.add(texts.eu_server_btn, texts.ru_server_btn)
# server_markup.add(texts.na_server_btn, texts.sea_server_btn)

# # Клавіатура скасування дії
# cancel_markup = {"EN": ReplyKeyboardMarkup(resize_keyboard=True, selective=True),
#                  "RU": ReplyKeyboardMarkup(resize_keyboard=True, selective=True)}
# cancel_markup["EN"].add(texts.cancel_btn["EN"])
# cancel_markup["RU"].add(texts.cancel_btn["RU"])
