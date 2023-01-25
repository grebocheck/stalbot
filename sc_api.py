import requests
import settings


class StalcraftAPI:
    exbo_url = "https://exbo.net"

    def __init__(self):
        self.url = "https://eapi.stalcraft.net"
        self.token = settings.APP_TOKEN
        self.u_token = settings.USER_TOKEN
        self.u_name = settings.USER_NAME
        self.region = "EU"

    def get_regions(self):
        params = {
            "Client-Id": str(settings.NUM_ID),
            "Client-Secret": settings.SECRET_KEY
        }
        r = requests.get(self.url + "/regions", headers=params)
        return r.json()

    def get_auction_lots(self, item: str):
        params = {
            "Client-Id": str(settings.NUM_ID),
            "Client-Secret": settings.SECRET_KEY
        }
        r = requests.get(self.url + "/%s/auction/%s/lots" % (self.region, item), headers=params)
        return r.json()

    def get_price_history(self, item: str):
        params = {
            "Client-Id": str(settings.NUM_ID),
            "Client-Secret": settings.SECRET_KEY
        }
        r = requests.get(self.url + "/%s/auction/%s/history" % (self.region, item), headers=params)
        return r.json()

    def get_characters(self):
        params = {
            "Authorization": self.u_name + " " + self.u_token,
        }
        r = requests.get(self.url + "/%s/characters" % self.region, headers=params)
        return r.json()

    def get_clan_info(self, clan_id: str):
        params = {
            "Authorization": self.u_name + " " + self.u_token,
        }
        r = requests.get(self.url + "/%s/clan/%s/info" % (self.region, clan_id), headers=params)
        return r.json()

    def get_clan_member(self, clan_id: str):
        params = {
            "Authorization": self.u_name + " " + self.u_token,
        }
        r = requests.get(self.url + "/%s/clan/%s/members" % (self.region, clan_id), headers=params)
        return r.json()

    def get_clans(self):
        params = {
            "Authorization": self.u_name + " " + self.u_token,
        }
        r = requests.get(self.url + "/%s/clans" % self.region, headers=params)
        return r.json()

    def get_emission(self):
        params = {
            "Client-Id": str(settings.NUM_ID),
            "Client-Secret": settings.SECRET_KEY
            # "Authorization": self.u_name + " " + self.u_token,
        }
        r = requests.get(self.url + "/%s/emission" % self.region, headers=params)
        return r.json()

    def get_friends(self, character: str):
        params = {
            "Authorization": self.u_name + " " + self.u_token,
        }
        r = requests.get(self.url + "/%s/friends/%s" % (self.region, character), headers=params)
        return r.json()
