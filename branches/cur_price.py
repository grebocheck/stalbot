from bot import *
from keyboards import *
import filters as flt


@dp.message_handler(flt.transFilter('Проверить цену💰'))
async def process_price_one(message: types.Message):
    user = message.from_user
    await Form_Check.get_item.set()
    await message.answer(await lng.trans("Введите название предмета📦", user),
                         reply_markup=await get_cancel_keyboard(user))


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Check.get_item)
async def process_price_two(message: types.Message, state: FSMContext):
    user = message.from_user
    user_lang = await lng.get_user_lang(user)
    it_item = dbitem.search_item_id_by_name(message.text, user_lang)
    user_server = await get_user_server(user)
    if it_item:
        await state.finish()
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_server)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
        plot, back_btn, next_btn = await worse.get_auc_lot(item_id=it_item, server=user_server,
                                                           lang=user_lang, image_path=image_path, page=0)
        if plot:
            keyboard = await get_cur_price_keyboard(next_btn=next_btn, back_btn=back_btn, page=0, item=it_item)
            await message.reply_photo(plot, caption=await lng.trans(
                "Цены на аукционе сервера {} сейчас на предмет {} ⚖", user,
                [user_server, item_name]),
                                             parse_mode="Markdown", reply_markup=keyboard)
            plot.close()
            os.remove("table.png")
            return
        else:
            return await message.reply(await lng.trans("На аукционе нет лотов для товара: {}", user, item_name))
    await message.reply(await lng.trans("Простите, но я не могу найти этот предмет😰", user),
                        reply_markup=await get_cancel_keyboard(user))


@dp.callback_query_handler(ft.Text(startswith='cur:'))
async def cnange_emission_callback(callback: types.CallbackQuery):
    user = callback.from_user
    user_lang = await lng.get_user_lang(user)
    user_server = await get_user_server(user)
    choice = callback.data.split(':')[1]
    page = int(callback.data.split(':')[2])
    if choice == '1':
        page += 1
    else:
        page -= 1
    it_item = callback.data.split(':')[3]
    image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_server)
    item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
    plot, back_btn, next_btn = await worse.get_auc_lot(item_id=it_item, server=user_server,
                                                       lang=user_lang, image_path=image_path, page=page)
    if plot:
        keyboard = await get_cur_price_keyboard(next_btn=next_btn, back_btn=back_btn, page=page, item=it_item)
        await callback.message.edit_media(media=types.InputMediaPhoto(plot),
                                          reply_markup=keyboard)
        plot.close()
        os.remove("table.png")
        return
    else:
        return await callback.message.reply(await lng.trans("На аукционе нет лотов для товара: {}",
                                                            user, item_name))
