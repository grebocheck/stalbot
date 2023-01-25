import aiohttp
import config


class StalcraftAPI:
    exbo_url = "https://exbo.net"
    url = "https://eapi.stalcraft.net"

    def __init__(self):
        self.app_id = str(config.client_id)
        self.app_secret = config.client_secret
        self.params = {
            "Client-Id": self.app_id,
            "Client-Secret": self.app_secret
        }

    async def get_regions(self):
        """
        Отримати назви серверів
        :return: Example [{'id': 'RU', 'name': 'RUSSIA'}, ...
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "/regions", headers=self.params) as r:
                return r.json()

    async def get_auction_lots(self, item: str, region: str):
        """
        Показати ціни на предмет на аукціоні
        :param item: str Ідентифікатор предмету (XXXX)
        :param region: str Назва серверу (EU)
        :return: Example {'total': 10, 'lots': [
                 {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-23T10:05:06.465068Z',
                        'endTime': '2023-01-23T22:05:06.465069Z', 'additional': {}}, ...
        """
        parm = {
            "sort": "buyout_price",
            "limit": 15,
            "order": "asc",
            "additional": "true"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "/%s/auction/%s/lots" % (region, item),
                                   headers=self.params, params=parm) as r:
                return await r.json()

    async def get_price_history(self, item: str, region: str):
        """
        Показати історію цін на предмет
        :param item: str Ідентифікатор предмету (XXXX)
        :param region: str Назва серверу (EU)
        :return: Example {'total': 10, 'prices': [{'amount': 1, 'price': 1000, 'time': '2023-01-23T12:09:15.842149Z'}, ...
        """
        parm = {
            "limit": 100,
            "additional": "true"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "/%s/auction/%s/history" % (region, item),
                                   headers=self.params, params=parm) as r:
                return await r.json()

    async def get_emission(self, region: str):
        """
        Отримати інформацію про останній викид
        :param region: str server id (EU)
        :return: Example {'currentStart': '2023-01-23T12:23:13Z',
                    'previousStart': '2023-01-23T10:21:13Z',
                    'previousEnd': '2023-01-23T10:26:13Z'}
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "/%s/emission" % region, headers=self.params) as r:
                return await r.json()
