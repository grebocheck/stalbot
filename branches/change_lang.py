from bot import *
from keyboards import *
import filters as flt


@dp.message_handler(flt.transFilter('Сменить язык 🌐'))
async def process_choose_notif_mode_one(message: types.Message):
    user = message.from_user
    await message.answer(await lng.trans("Выберите язык🌐", user),
                         reply_markup=kbLang)
