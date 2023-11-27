import keyboards
from bot import *
from branches import main, history, cur_price, emission, admin
from additions.apio import scb
import asyncio


# init
async def initialize(data):
    info = await data.bot.me
    log_inf(f'ID: {info["id"]}')
    log_inf(f'Username: {info["username"]}')
    await scb.run()
    # for a in keyboards.regions:
    #     region = a['id']
    #     asyncio.ensure_future(emission.emission_logger(region=region))
    asyncio.ensure_future(emission.good_finder(region='RU'))


# logging
if __name__ == "__main__":
    while True:
        try:
            log_inf("Бот запущений!")
            executor.start_polling(dp, on_startup=initialize, skip_updates=True)
        except Exception as ex:
            log_err(str(ex))
            time.sleep(15)
