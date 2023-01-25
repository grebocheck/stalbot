import api_sc
import asyncio
import worse

scb = api_sc.StalcraftAPI()


async def main():
    print(await scb.get_price_history())

