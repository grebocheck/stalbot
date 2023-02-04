import config
from bot import *
from keyboards import *
import filters as flt


@dp.message_handler(commands=['statistic'], state='*')
async def get_statistic_proccess(message: types.Message):
    if message.from_user.id in config.admin_list:
        user = message.from_user
        all_users = await get_all_users()
        en_lang = 0
        ua_lang = 0
        ru_lang = 0
        eu_serv = 0
        ru_serv = 0
        na_serv = 0
        sea_serv = 0
        emission_count = 0
        users_count = 0
        for a in all_users:
            users_count += 1

            if a[3]:
                emission_count += 1

            if a[1] == "EU":
                eu_serv += 1
            elif a[1] == "RU":
                ru_serv += 1
            elif a[1] == "NA":
                na_serv += 1
            elif a[1] == "SEA":
                sea_serv += 1

            if a[2] == "uk":
                ua_lang += 1
            elif a[2] == "en":
                en_lang += 1
            elif a[2] == "ru":
                ru_lang += 1

        text = await lng.trans("Статистика\nВсего пользователей: %d\nОповещения о выбросах: %d\n\nСервера\nEU: "
                               "%d\nRU: %d\nNA: %d\nSEA: %d\n\nЯзыки:\nEN: %d\nUA: %d\nRU: %dа", user) % (
            users_count,
            emission_count,
            eu_serv,
            ru_serv,
            na_serv,
            sea_serv,
            en_lang,
            ua_lang,
            ru_lang)

        await message.answer(text)


@dp.message_handler(commands=['send_all'])
async def process_send_all_command(message: types.Message, state: FSMContext):
    if message.from_user.id in config.admin_list:
        user = message.from_user
        await Form_Send.get_mess.set()
        users = await get_all_users()
        user_id_mass = []
        for a in users:
            user_id_mass.append(a[0])
        async with state.proxy() as data:
            data['mass_id'] = user_id_mass
        await message.reply(await lng.trans("Отправь мне сообщение для рассылки", user),
                            reply_markup=await get_cancel_keyboard(user))


@dp.message_handler(content_types=ContentType.all(), state=Form_Send.get_mess)
async def process_send_all_step_two(message: types.Message, state: FSMContext):
    """
    Команда рассылки пользователям бота
    Вторая стадия - Рассылка и отчет
    """
    async with state.proxy() as data:
        user_id_mass = data['mass_id']
    await state.finish()
    num_users = len(user_id_mass)
    num_succ = 0
    for a in user_id_mass:
        try:
            await message.copy_to(a)
            num_succ += 1
        except:
            pass
    text = await lng.trans("Готово, отправлено") + f" {num_succ}/{num_users}"
    await message.answer(text)

