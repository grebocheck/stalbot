import worse
from bot import *
from keyboards import *


@dp.message_handler(lambda message: message.text == "Перевірити ціну💰")
async def process_choose_notif_mode_one(message: types.Message):
    user = message.from_user
    await Form_Check.get_item.set()
    await message.answer(await lng.trans("Введите название предмета📦", user),
                         reply_markup=await get_cancel_keyboard(user))


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Check.get_item)
async def process_choose_notif_mode_two(message: types.Message, state: FSMContext):
    user = message.from_user
    user_lang = await lng.get_user_lang(user)
    it_item = dbitem.search_item_id_by_name(message.text, user_lang)
    user_server = "EU"
    if it_item:
        await state.finish()
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name=user_server)
        item_name = dbitem.search_item_name_by_id(it_item, server_name=user_server, lang=user_lang)
        plot = await worse.get_auc_lot(item_id=it_item, server=user_server,
                                       lang=user_lang, image_path=image_path)
        await message.reply_photo(plot, caption=await lng.trans("Цены на аукционе сервера {} сейчас на предмет {} ⚖", user,
                                                                [user_server, item_name]),
                                  parse_mode="Markdown", reply_markup=await get_main_keyboard(user))
    else:
        await message.reply("Тут текст что предмет не найден")
