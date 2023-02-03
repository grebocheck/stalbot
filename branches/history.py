import os

from bot import *
from keyboards import *
import filters as flt


@dp.message_handler(flt.transFilter("Історія цін 📈"))
async def process_history_one(message: types.Message):
    user = message.from_user
    await Form_Hist.get_time.set()
    await message.answer(await lng.trans("Выберите за какое время хотите получить график ⏳", user),
                         reply_markup=await get_choose_time_keyboard(user))


@dp.callback_query_handler(ft.Text(startswith='htime:'), state=Form_Hist.get_time)
async def process_history_three(callback: types.CallbackQuery, state: FSMContext):
    user = callback.from_user
    choice = callback.data.split('htime:')[1]
    if choice == "0":
        days_lim = None
    elif choice == "1":
        days_lim = 7
    elif choice == "2":
        days_lim = 30
    else:
        days_lim = 90
    async with state.proxy() as data:
        data["days_lim"] = days_lim
    await bot.delete_message(user.id, message_id=callback.message.message_id)
    await bot.send_message(user.id, "Введите название предмета📦",
                           reply_markup=await get_cancel_keyboard(user))
    await Form_Hist.next()


@dp.callback_query_handler(ft.Text(startswith='his:'), state=Form_Hist.get_item)
@dp.message_handler(content_types=ContentType.TEXT, state=Form_Hist.get_item)
async def process_history_three(message, state: FSMContext):
    user = message.from_user
    user_lang = await lng.get_user_lang(user)
    user_server = await get_user_server(user)
    if type(message) == types.Message:
        it_items = dbitem.search_item_id_by_name(message.text, user_server, user_lang)
        if len(it_items.keys()) > 1:
            kb = await get_history_price_keyboard(it_items)
            return await message.reply(await lng.trans('Нашёл несколько вариантов, выберете ниже', user),
                                       reply_markup=kb)
        elif len(it_items.keys()) == 0:
            it_item = None
        else:
            it_item = list(it_items.values())[0]
    else:
        choice = message.data.split('his:')[1]
        it_item = choice
        await bot.delete_message(user.id, message.message.message_id)

    async with state.proxy() as data:
        days_lim = data["days_lim"]
    await state.finish()

    if it_item:
        soon_mess = await bot.send_message(user.id, await lng.trans("Рисую график 🎨", user))
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_server)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
        plot = await worse.get_history(item_id=it_item, server=user_server, lang=user_lang,
                                       item_name=item_name, image_path=image_path, days_lim=days_lim)
        await soon_mess.delete()
        media = types.MediaGroup()
        for a in plot:
            media.attach_photo(types.InputMediaPhoto(open(a, "rb")))
        await bot.send_media_group(user.id, media=media,
                                   # caption=await lng.trans("История цен на {} на сервере {}📊", user,
                                   #                         [item_name, user_server]),
                                   # parse_mode="Markdown", reply_markup=await get_main_keyboard(user)
                                   )
        # for a in plot:
        #     os.remove(a)
    else:
        await bot.send_message(user.id, await lng.trans("Простите, но я не могу найти этот предмет😰", user))
