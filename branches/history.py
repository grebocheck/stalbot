from bot import *
from keyboards import *


@dp.message_handler(lambda message: message.text == "Історія цін 📈")
async def process_choose_notif_mode_one(message: types.Message):
    user = message.from_user
    await Form_Hist.get_item.set()
    await message.answer("Тут будет текст о истории цен", reply_markup=await get_cancel_keyboard(user))


@dp.message_handler(content_types=ContentType.TEXT, state=Form_Hist.get_item)
async def process_choose_notif_mode_two(message: types.Message, state: FSMContext):
    user = message.from_user
    user_lang = await lng.get_user_lang(user)
    it_item = dbitem.search_item_id_by_name(message.text, user_lang)
    if it_item:
        await state.finish()
        image_path = dbitem.get_item_image(my_item_id=it_item, server_name="EU")
        item_name = dbitem.search_item_name_by_id(it_item, server_name="EU", lang=user_lang)
        plot = await worse.get_history(item_id=it_item, server="EU", lang=user_lang,
                                       item_name=item_name, image_path=image_path)

        await message.reply_photo(plot, caption="График",
                                  parse_mode="Markdown", reply_markup=await get_main_keyboard(user))
