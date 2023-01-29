import aiohttp


class StalcraftAPI:

    def __init__(self, client_id, client_secret, url="https://eapi.stalcraft.net/"):
        self.__api_url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.appToken = 'UnAuthorizated'
        self.authHeader = {"Authorization": f"Bearer {self.appToken}"}
        self.session = aiohttp.ClientSession()

    async def __request_get(self, endpoint, headers=None, apiUrl=None, method='get'):
        apiUrl = apiUrl if apiUrl else self.__api_url
        url = apiUrl + endpoint
        if method == 'post':
            async with self.session.post(url, data=headers) as resp:
                r = await resp.json()
        else:
            async with self.session.get(url, headers=headers) as resp:
                r = await resp.json()
        return r

    async def get_regions(self):
        endpoint = 'regions'
        r = await self.__request_get(endpoint, self.authHeader)
        return r

    async def get_auction_history(self, item_id, region, additional="true", limit=100, offset=0):
        endpoint = f'{region}/auction/{item_id}/history'
        params = f'?limit={limit}&additional={additional}&offset={offset}'
        endpoint += params
        r = await self.__request_get(endpoint, self.authHeader)
        return r

    async def get_auction_lots(self, item_id, region, additional="true", limit=20, offset=0):
        endpoint = f'{region}/auction/{item_id}/lots'
        params = f'?limit={limit}&sort=buyout_price&offset={offset}&order=asc&additional={additional}'
        endpoint += params
        r = await self.__request_get(endpoint, self.authHeader)
        return r

    async def get_emission(self, region):
        endpoint = f'{region}/emission'
        r = await self.__request_get(endpoint, self.authHeader)
        return r

    async def run(self):
        endpoint = 'oauth/token'
        headers = {
            "client_id": str(self.client_id),
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        r = await self.__request_get(endpoint, headers, apiUrl='https://exbo.net/', method='post')
        self.appToken = r.get('access_token')
        self.authHeader = {"Authorization": f"Bearer {self.appToken}"}
        return r

    async def close(self):
        await self.session.close()
