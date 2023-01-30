import os

from bot import *
from keyboards import *
import filters as flt


@dp.message_handler(flt.transFilter("Історія цін 📈"))
async def process_history_one(message: types.Message):
    user = message.from_user
    await Form_Hist.get_item.set()
    await message.answer(await lng.trans("Введите название предмета📦", user),
                         reply_markup=await get_cancel_keyboard(user))


@dp.callback_query_handler(ft.Text(startswith='his:'), state='*')
@dp.message_handler(content_types=ContentType.TEXT, state=Form_Hist.get_item)
async def process_history_two(message: types.Message | types.CallbackQuery, state: FSMContext):
    await state.finish()
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
    if it_item:
        soon_mess = await bot.send_message(user.id, await lng.trans("Рисую график 🎨", user))
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_server)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
        plot = await worse.get_history(item_id=it_item, server=user_server, lang=user_lang,
                                       item_name=item_name, image_path=image_path)
        await soon_mess.delete()
        media = types.MediaGroup()
        for a in plot:
            media.attach_photo(types.InputMediaPhoto(open(a, "rb")))
        await bot.send_media_group(user.id, media=media,
                                   # caption=await lng.trans("История цен на {} на сервере {}📊", user,
                                   #                         [item_name, user_server]),
                                   # parse_mode="Markdown", reply_markup=await get_main_keyboard(user)
                                   )
        for a in plot:
            os.remove(a)
    else:
        await bot.send_message(user.id, await lng.trans("Простите, но я не могу найти этот предмет😰", user))
