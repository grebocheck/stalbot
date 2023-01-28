from bot import *
from branches import main, history, cur_price, emission
from additions.apio import scb
import threading


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
            threading.Thread(target=emission.emission_loop, daemon=True).start()
            executor.start_polling(dp, on_startup=initialize, skip_updates=True)
        except Exception as ex:
            log_err(str(ex))
            time.sleep(15)