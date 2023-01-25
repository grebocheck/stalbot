import os
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, BotCommand, \
    ChatActions, video_note, ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiogram.utils.exceptions

import dbitem
import settings
import texts
from loge import log_deb, log_err, log_inf
import botdb
import worse


bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Updates were skipped successfully.')
    return


# Клавіатура меню
menu_markup = {"EN": types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True),
               "RU": types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)}
# EN меню
menu_markup["EN"].add(texts.get_history_price["EN"], texts.get_check_price["EN"])
menu_markup["EN"].add(texts.about_us_btn["EN"], texts.notif_emiss["EN"])
menu_markup["EN"].add(texts.update_language["EN"], texts.update_server["EN"])
# RU меню
menu_markup["RU"].add(texts.get_history_price["RU"], texts.get_check_price["RU"])
menu_markup["RU"].add(texts.about_us_btn["RU"], texts.notif_emiss["RU"])
menu_markup["RU"].add(texts.update_language["RU"], texts.update_server["RU"])

# Прибрати клавіатуру
remove_mark = types.ReplyKeyboardRemove()

# Клавіатура мов
lang_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
lang_markup.add(texts.en_lang_btn, texts.ru_lang_btn)

# Клавіатура серверів
server_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
server_markup.add(texts.eu_server_btn, texts.ru_server_btn)
server_markup.add(texts.na_server_btn, texts.sea_server_btn)

# Клавіатура скасування дії
cancel_markup = {"EN": types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True),
                 "RU": types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)}
cancel_markup["EN"].add(texts.cancel_btn["EN"])
cancel_markup["RU"].add(texts.cancel_btn["RU"])


# форма реєстрації
class Form_Reg(StatesGroup):
    get_lang = State()
    get_serv = State()


# форма зміни мови інтерфейсу
class Form_Lang(StatesGroup):
    get_lang = State()


# форма зміни серверу
class Form_Serv(StatesGroup):
    get_serv = State()


# форма отримання історії цін на предмет
class Form_Hist(StatesGroup):
    get_item = State()


# форма отримання цін на предмет на аукціоні
class Form_Check(StatesGroup):
    get_item = State()


# форма налаштуваннь сповіщень про викиди
class Form_Notif(StatesGroup):
    get_mode = State()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals=[texts.cancel_btn["EN"], texts.cancel_btn["RU"]], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Функція скасування будь-якої дії
    """
    if botdb.extend_user(message.from_user.id):
        it_user = botdb.get_user(message.from_user.id)
    else:
        await state.finish()
        await message.reply(texts.need_reg, reply_markup=remove_mark)
        return
    current_state = await state.get_state()
    if current_state is None:
        await message.reply(texts.menu_text[it_user.lang], reply_markup=menu_markup[it_user.lang])
        return
    await state.finish()
    await message.reply(texts.cancel_success[it_user.lang], reply_markup=menu_markup[it_user.lang])


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    """
    Стартова функція, розпочинає реєстрацію або повертає меню користувачу
    Стадія перша - запит на вибір мови з клавіатури
    """
    await state.finish()
    if botdb.extend_user(message.from_user.id):
        it_user = botdb.get_user(message.from_user.id)
        await message.reply(texts.menu_text, reply_markup=menu_markup[it_user.lang])
    else:
        await Form_Reg.get_lang.set()
        await message.reply(texts.start_mess, parse_mode="Markdown", reply_markup=lang_markup)


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Reg.get_lang)
async def process_reg_two(message: types.Message, state: FSMContext):
    """
    Реєстрація
    Стадія друга - отримання мови, запит на вибір серверу.
    """
    if message.text in texts.langs_btn:
        if message.text == texts.en_lang_btn:
            lang = "EN"
        else:
            lang = "RU"
        async with state.proxy() as data:
            data['lang'] = lang
        await Form_Reg.next()
        await message.reply(texts.choose_server[lang], reply_markup=server_markup)
    else:
        await message.reply(texts.choose_incorect_lang, reply_markup=lang_markup)


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Reg.get_serv)
async def process_reg_three(message: types.Message, state: FSMContext):
    """
    Реєстрація
    Стадія третя - вибір серверу та завершення реєстрації
    """
    async with state.proxy() as data:
        lang = data['lang']
    if message.text in texts.servers_btn:
        if message.text == texts.eu_server_btn:
            server = "EU"
        elif message.text == texts.ru_server_btn:
            server = "RU"
        elif message.text == texts.na_server_btn:
            server = "NA"
        else:
            server = "SEA"
        it_user = botdb.User(user_id=message.from_user.id,
                             username=message.from_user.username,
                             fullname=message.from_user.full_name,
                             lang=lang,
                             server_name=server)
        it_user.insert_user()
        await state.finish()
        await message.reply(texts.success_reg[lang], reply_markup=menu_markup[lang])
    else:
        await message.reply(texts.choose_incorect[lang], reply_markup=server_markup)


@dp.message_handler(lambda message: not botdb.extend_user(message.from_user.id))
async def process_stop_unreg(message: types.Message):
    """
    Зупиняє незареєстованого користувача та повертає його на пункт реєстрації
    """
    await message.reply(texts.need_reg, reply_markup=remove_mark)


@dp.message_handler(lambda message: message.text in [texts.update_language["EN"], texts.update_language["RU"]])
async def process_change_lang_one(message: types.Message):
    """
    Функція зміни мови інтерфейсу для користувача
    Стадія перша - запит на вибір мови
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    await Form_Lang.get_lang.set()
    await message.reply(texts.choose_lang[lang], reply_markup=lang_markup)


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Lang.get_lang)
async def process_change_lang_two(message: types.Message, state: FSMContext):
    """
    Функція зміни мови інтерфейсу для користувача
    Стадія друга - зміна мови
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    if message.text in texts.langs_btn:
        if message.text == texts.en_lang_btn:
            lang = "EN"
        else:
            lang = "RU"
        it_user.lang = lang
        it_user.update_lang()
        await state.finish()
        await message.reply(texts.success_choose[lang], reply_markup=menu_markup[lang])
    else:
        await message.reply(texts.choose_incorect[lang], reply_markup=lang_markup)


@dp.message_handler(lambda message: message.text in [texts.update_server["EN"], texts.update_server["RU"]])
async def process_change_server_one(message: types.Message):
    """
    Функція зміни серверу користувача
    Стадія перша - запит на вибір серверу
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    await Form_Serv.get_serv.set()
    await message.reply(texts.choose_server[lang], reply_markup=server_markup)


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Serv.get_serv)
async def process_change_server_two(message: types.Message, state: FSMContext):
    """
    Функція зміни серверу користувача
    Стадія друга - зміна сервера
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    if message.text in texts.servers_btn:
        if message.text == texts.eu_server_btn:
            server = "EU"
        elif message.text == texts.ru_server_btn:
            server = "RU"
        elif message.text == texts.na_server_btn:
            server = "NA"
        else:
            server = "SEA"
        it_user.server_name = server
        it_user.update_server()
        await state.finish()
        await message.reply(texts.success_choose[lang], reply_markup=menu_markup[lang])
    else:
        await message.reply(texts.choose_incorect[lang], reply_markup=server_markup)


@dp.message_handler(lambda message: message.text in [texts.notif_emiss["EN"], texts.notif_emiss["RU"]])
async def process_choose_notif_mode_one(message: types.Message):
    """
    Функція налаштування сповіщень про викиди
    Стадія перша - запит на вибір режиму
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang

    emiss_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    emiss_markup.add(texts.btn_one, texts.btn_two)
    if botdb.extend_notif(message.from_user.id):
        emiss_markup.add(texts.notif_stop_btn[lang])
    emiss_markup.add(texts.cancel_btn[lang])

    await Form_Notif.get_mode.set()
    await message.reply(texts.notif_emiss_choose[lang], reply_markup=emiss_markup)


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Notif.get_mode)
async def process_choose_notif_mode_two(message: types.Message, state: FSMContext):
    """
    Функція налаштування сповіщень про викиди
    Стадія друга - зміна режиму
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    if message.text in [texts.btn_one, texts.btn_two, texts.notif_stop_btn[lang]]:
        if botdb.extend_notif(message.from_user.id):
            it_notif = botdb.get_notif(message.from_user.id)
            if message.text == texts.btn_one:
                it_notif.mode = 1
                it_notif.upd_mode()
            elif message.text == texts.btn_two:
                it_notif.mode = 2
                it_notif.upd_mode()
            else:
                it_notif.del_notif()
        else:
            if message.text == texts.btn_one:
                notif_mode = 1
                notife = botdb.Notif(message.from_user.id, mode=notif_mode)
                notife.insert_notif()
            elif message.text == texts.btn_two:
                notif_mode = 2
                notife = botdb.Notif(message.from_user.id, mode=notif_mode)
                notife.insert_notif()
        await state.finish()
        await message.reply(texts.success_choose[lang], reply_markup=menu_markup[lang])
    else:
        await message.reply(texts.choose_incorect[lang])


@dp.message_handler(lambda message: message.text in [texts.about_us_btn["EN"], texts.about_us_btn["RU"]])
async def process_choose_notif_mode_one(message: types.Message):
    """
    Виведення інформації про бота
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    await message.reply(texts.about_us_text[lang], reply_markup=menu_markup[lang])


@dp.message_handler(lambda message: message.text in [texts.get_check_price["EN"], texts.get_check_price["RU"]])
async def process_choose_notif_mode_one(message: types.Message):
    """
    Вивести ціну на товар
    Стадія перша - запит на назву товару
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    await Form_Check.get_item.set()
    await message.reply(texts.get_item[lang], reply_markup=cancel_markup[lang])


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Check.get_item)
async def process_choose_notif_mode_two(message: types.Message, state: FSMContext):
    """
    Вивести ціну на товар
    Стадія друга - виведеня інформації про ціни
    """
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    it_item = dbitem.search_item_id_by_name(message.text, it_user.server_name)
    if it_item:
        await state.finish()
        prices = await worse.get_auc_lot(item_id=it_item, server=it_user.server_name, lang=lang)
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=it_user.server_name)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=it_user.server_name)
        text_mess = texts.now_prices[lang] % (it_user.server_name, item_name[lang], prices)
        await message.reply_photo(open(image_path, "rb"), caption=text_mess,
                                  parse_mode="Markdown", reply_markup=menu_markup[lang])
    else:
        await message.reply(texts.not_found_item[lang])


@dp.message_handler(lambda message: message.text in [texts.get_history_price["EN"], texts.get_history_price["RU"]])
async def process_choose_notif_mode_one(message: types.Message):
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    await Form_Hist.get_item.set()
    await message.reply(texts.get_item[lang], reply_markup=cancel_markup[lang])


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Hist.get_item)
async def process_choose_notif_mode_two(message: types.Message, state: FSMContext):
    it_user = botdb.get_user(message.from_user.id)
    lang = it_user.lang
    it_item = dbitem.search_item_id_by_name(message.text, it_user.server_name)
    if it_item:
        await state.finish()
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=it_user.server_name)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=it_user.server_name)
        plot = await worse.get_history(item_id=it_item, server=it_user.server_name, lang=lang,
                                       item_name=item_name[lang], image_path=image_path)

        await message.reply_photo(plot, caption=texts.hist_text[lang] % (item_name[lang], it_user.server_name),
                                  parse_mode="Markdown", reply_markup=menu_markup[lang])
    else:
        await message.reply(texts.not_found_item[lang])


if __name__ == "__main__":
    while True:
        try:
            log_inf("Бот запущений!")
            executor.start_polling(dp, skip_updates=True)
        except Exception as ex:
            log_err(str(ex))
            time.sleep(15)
