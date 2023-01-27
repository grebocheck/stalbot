from bot import *
from branches import main, history, cur_price, emission, change_server, change_lang
from additions.apio import scb


#init
async def initialize(data):
    info = await data.bot.me
    log_inf(f'ID: {info["id"]}')
    log_inf(f'Username: {info["username"]}')
    await scb.run()


#logging
if __name__ == "__main__":
    while True:
        try:
            log_inf("Бот запущений!")
            executor.start_polling(dp, on_startup=initialize, skip_updates=True)
        except Exception as ex:
            log_err(str(ex))
            time.sleep(15)