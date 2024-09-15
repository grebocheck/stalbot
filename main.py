from additions.items_update import update_stalcraft_database_items, update_stalcraft_database_items_loop
import asyncio, os
from config import repo_dir
from additions.log import log_inf

if not os.path.exists(repo_dir):
    log_inf(f'start downloading database')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_stalcraft_database_items())
    log_inf(f'complete downloading database')

from bot import log_inf, executor, dp, log_err
from branches import main, history, cur_price, emission, admin
from additions.apio import scb

import time


# init
async def initialize(data):
    info = await data.bot.me
    log_inf(f'ID: {info["id"]}')
    log_inf(f'Username: {info["username"]}')
    asyncio.ensure_future(update_stalcraft_database_items_loop())
    await scb.run()
    import keyboards
    for a in keyboards.regions:
        region = a['id']
        asyncio.ensure_future(emission.emission_logger(region=region))



# logging
if __name__ == "__main__":
    while True:
        try:
            log_inf("Бот запущений!")
            executor.start_polling(dp, on_startup=initialize, skip_updates=True)
        except Exception as ex:
            log_err(str(ex))
            time.sleep(15)
