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
    await state.finish()
    if it_item:
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_server)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
        plot = await worse.get_auc_lot(item_id=it_item, server=user_server,
                                       lang=user_lang, image_path=image_path)
        if plot:
            return await message.reply_photo(plot, caption=await lng.trans("Цены на аукционе сервера {} сейчас на предмет {} ⚖", user,
                                                                    [user_server, item_name]),
                                    parse_mode="Markdown", reply_markup=await get_main_keyboard(user))
        else:
            return await message.reply(await lng.trans("На аукционе нет лотов для товара: {}", user, item_name))
    await message.reply(await lng.trans("Простите, но я не могу найти этот предмет😰", user))
