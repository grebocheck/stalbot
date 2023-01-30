import asyncio

from bot import *
from keyboards import *
import filters as flt
from additions.apio import scb


async def emission_logger(region):
    try:
        log_inf("RUN EMISSION LOOP " + region)
        while True:
            emiss = await scb.get_emission(region=region)
            if 'currentStart' not in emiss:
                await asyncio.sleep(10)
                continue
            log_deb(f"EMISSION IN {region}")
            users = await get_all_users_emission()
            for user in users:
                user_server = await get_user_server(user)
                if user_server != region:
                    continue
                try:
                    await bot.send_message(user.id,
                                           await lng.trans("На сервере {} начался выброс🌩", user, user_server),
                                           reply_markup=await get_emission_close_keyboard(user))
                except Exception as ex:
                    log_err(str(ex))
            await asyncio.sleep(2.5 * 60 * 60)
    except Exception as ex:
        log_err(str(ex))
