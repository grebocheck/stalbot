import asyncio

import aiogram.utils.exceptions

from bot import *
from keyboards import *
import filters as flt
from datetime import datetime, timezone, timedelta
from additions.apio import scb


async def emission_logger(region):
    log_inf("RUN EMISSION LOOP " + region)
    while True:
        try:
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
                except (aiogram.utils.exceptions.BotBlocked, aiogram.utils.exceptions.UserDeactivated):
                    await db.userSettings.update_one(
                        {
                            'telegram_id': user.id
                        },
                        {
                            '$set': {
                                'emission': False
                            }
                        }, True)
                except Exception as ex:
                    log_err(str(ex))
            await asyncio.sleep(2.5 * 60 * 60)
        except Exception as ex:
            log_err(str(ex))


async def good_finder(region):
    log_inf("RUN SECRET GOOD FINDER LOOP OF " + region)
    item_list = dbitem.good_item_list(server_name='RU', user_lang='ru')
    log_deb(f"Length: {len(item_list)}")
    passed_list = []
    while True:
        await asyncio.sleep(5)
        for item in item_list:
            try:
                await asyncio.sleep(1)
                log_deb(item)
                lots = await scb.get_auction_lots(item_id=item_list[item], region="RU", limit=20, order="desc", select="time_left")

                if not 'lots' in lots:
                    continue

                min_buyout = 10**12
                for lot in lots['lots']:

                    if min_buyout > int(lot['buyoutPrice']):
                        min_buyout = int(lot['buyoutPrice'])

                for lot in lots['lots']:
                    date = datetime.strptime(lot['endTime'] + "+0000",
                                             "%Y-%m-%dT%H:%M:%SZ%z") - datetime.now(timezone.utc).replace(microsecond=0)
                    reaction_time = timedelta(hours=1)
                    if date > reaction_time:
                        continue
                    if 'currentPrice' in lot:
                        startPrice = int(lot['currentPrice'])
                    else:
                        startPrice = int(lot['startPrice'])
                    buyoutPrice = int(lot['buyoutPrice'])
                    amount = int(lot['amount'])

                    if startPrice < min_buyout * 0.7 and not lot["endTime"] in passed_list:
                        passed_list.append(lot["endTime"])
                        seconds = round(date.total_seconds())
                        hours = round(seconds // 3600)
                        minutes = round((seconds - hours * 3600) // 60)
                        sec = seconds - hours * 3600 - minutes * 60

                        date_str = "%02d:%02d %02d с" % (hours, minutes, sec)
                        await bot.send_message(-1001951283691, f"""{item} ({amount})
Ставка: {startPrice}
Выкуп: {buyoutPrice}
Осталось времени: {date_str}""")
            except Exception as ex:
                print(ex)
                await asyncio.sleep(10)


