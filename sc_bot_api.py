import requests
import settings


class StalcraftAPI:
    exbo_url = "https://exbo.net"
    url = "https://eapi.stalcraft.net"

    def __init__(self):
        self.app_id = str(settings.NUM_ID)
        self.app_secret = settings.SECRET_KEY
        self.params = {
            "Client-Id": self.app_id,
            "Client-Secret": self.app_secret
        }

    def get_regions(self):
        """
        Get server regions
        :return: Example [{'id': 'RU', 'name': 'RUSSIA'}, ...
        """
        r = requests.get(self.url + "/regions", headers=self.params)
        return r.json()

    def get_auction_lots(self, item: str, region: str):
        """
        Select items in auction by id (XXXX)
        :param item: str id (XXXX)
        :param region: str server id (EU)
        :return: Example {'total': 10, 'lots': [
                 {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-23T10:05:06.465068Z',
                        'endTime': '2023-01-23T22:05:06.465069Z', 'additional': {}}, ...
        """
        r = requests.get(self.url + "/%s/auction/%s/lots" % (region, item), headers=self.params)
        return r.json()

    def get_price_history(self, item: str, region: str):
        """
        Get price history in auction by id (XXXX)
        :param item: str id (XXXX)
        :param region: str server id (EU)
        :return: Example {'total': 10, 'prices': [{'amount': 1, 'price': 1000, 'time': '2023-01-23T12:09:15.842149Z'}, ...
        """
        parm = {
            "limit": 100
        }
        r = requests.get(self.url + "/%s/auction/%s/history" % (region, item), headers=self.params, params=parm)
        return r.json()

    def get_emission(self, region: str):
        """
        Get last emission
        :param region: str server id (EU)
        :return: Example {'currentStart': '2023-01-23T12:23:13Z',
                    'previousStart': '2023-01-23T10:21:13Z',
                    'previousEnd': '2023-01-23T10:26:13Z'}
        """
        r = requests.get(self.url + "/%s/emission" % region, headers=self.params)
        return r.json()
