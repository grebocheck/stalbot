from bot import *
from keyboards import *
import filters as flt


@dp.message_handler(flt.transFilter('Проверить цену💰'))
async def process_price_one(message: types.Message):
    user = message.from_user
    await Form_Check.get_item.set()
    await message.answer(await lng.trans("Введите название предмета📦", user),
                         reply_markup=await get_cancel_keyboard(user))


@dp.callback_query_handler(ft.Text(startswith='auc:'), state='*')
@dp.message_handler(content_types=ContentType.TEXT, state=Form_Check.get_item)
async def process_price_two(message, state: FSMContext):
    await state.finish()
    user = message.from_user
    user_lang = await lng.get_user_lang(user)
    user_server = await get_user_server(user)
    if type(message) == types.Message:
        it_items = dbitem.search_item_id_by_name(message.text, user_server, user_lang)
        if len(it_items.keys()) > 1:
            kb = await get_auc_price_keyboard(it_items)
            return await message.reply(await lng.trans('Нашёл несколько вариантов, выберете ниже', user), reply_markup=kb)
        elif len(it_items.keys()) == 0:
            it_item = None
        else:
            it_item = list(it_items.values())[0]
    else:
        choice = message.data.split('auc:')[1]
        it_item = choice
        await bot.delete_message(user.id, message.message.message_id)
    
    if it_item:
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_lang)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
        plot, back_btn, next_btn = await worse.get_auc_lot(item_id=it_item, server=user_server,
                                                           lang=user_lang, image_path=image_path,
                                                           page=0, item_name=item_name,
                                                           select="buyout_price", order=True)
        if plot:
            keyboard = await get_cur_price_keyboard(next_btn=next_btn, back_btn=back_btn, page=0,
                                                    item=it_item, select="buyout_price", order=True,
                                                    user=user)
            await bot.send_photo(user.id, plot, parse_mode="Markdown", reply_markup=keyboard)
            plot.close()
            os.remove("table.png")
            return
        else:
            return await bot.send_message(user.id, await lng.trans("На аукционе нет лотов для товара: {}", user, item_name))
    await bot.send_message(user.id, await lng.trans("Простите, но я не могу найти этот предмет😰", user),
                        reply_markup=await get_cancel_keyboard(user))


@dp.callback_query_handler(ft.Text(startswith='cur:'))
async def cnange_emission_callback(callback: types.CallbackQuery):
    user = callback.from_user
    user_lang = await lng.get_user_lang(user)
    user_server = await get_user_server(user)
    choice = callback.data.split(':')[1]
    page = int(callback.data.split(':')[2])
    it_item = callback.data.split(':')[3]
    select = callback.data.split(':')[4]
    order_call = callback.data.split(':')[5]
    if order_call == '1':
        order = True
    else:
        order = False

    if choice == 'next':
        page += 1
    elif choice == 'back':
        page -= 1
    elif choice == select:
        order = not order
    else:
        select = choice
    image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_server)
    item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
    plot, back_btn, next_btn = await worse.get_auc_lot(item_id=it_item, server=user_server,
                                                       lang=user_lang, image_path=image_path,
                                                       page=page, item_name=item_name,
                                                       select=select, order=order)
    if plot:
        keyboard = await get_cur_price_keyboard(next_btn=next_btn, back_btn=back_btn, page=page,
                                                item=it_item, select=select, order=order,
                                                user=user)
        text = await lng.trans(
            "Цены на аукционе сервера {} сейчас на предмет {} ⚖", user, [user_server, item_name])
        await callback.message.edit_media(media=types.InputMediaPhoto(plot, caption=text),
                                          reply_markup=keyboard)
        plot.close()
        os.remove("table.png")
        return
    else:
        return await callback.message.reply(await lng.trans("На аукционе нет лотов для товара: {}",
                                                            user, item_name))
