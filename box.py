import sc_bot_api
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt

sca = sc_bot_api.StalcraftAPI()

class Emission:
    def __init__(self, emiss):
        self.em_start = datetime.strptime(emiss["previousStart"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")
        self.em_stop = datetime.strptime(emiss["previousEnd"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")

    def time_ago(self) -> timedelta:
        """
        Time has elapsed since the emission
        :return: timedelta
        """
        now = datetime.now(timezone.utc)
        ago_time = now - self.em_stop
        return ago_time


class AuctionLot:
    def __init__(self, lot):
        self.item_id = lot["itemId"]
        self.start_price = int(lot["startPrice"])
        self.out_price = int(lot["buyoutPrice"])
        self.t_start = datetime.strptime(lot["startTime"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")
        self.t_stop = datetime.strptime(lot["endTime"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")


class HistoryLot:
    def __init__(self, hist, item_id, region):
        self.region = region
        self.item_id = item_id
        self.amount = hist["total"]
        self.prices = hist["prices"]

    def create_plot_prices(self):
        """
        Create plot
        :return: img
        """
        y = []
        x = []
        for a in self.prices:
            y.append(a["price"])
            x.append(datetime.strptime(a["time"] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
        plt.plot(x, y, marker='o', markerfacecolor='green', markersize=5)
        plt.xticks(rotation=20)
        plt.xlabel('Time')
        plt.ylabel('Price, Rub')
        plt.title(f'Price of {self.item_id} on {self.region}')
        plt.show()


class GameItem:
    pass


# emi = Emission(sca.get_emission("EU"))
# emi = Emission({'previousStart': '2023-01-23T13:53:18Z', 'previousEnd': '2023-01-23T13:58:18Z'})

# history = {'total': 10, 'prices': [{'amount': 1, 'price': 1200000, 'time': '2023-01-23T14:43:51Z'}, {'amount': 1, 'price': 1100000, 'time': '2023-01-18T10:23:02Z'}, {'amount': 1, 'price': 1200000, 'time': '2023-01-17T12:29:47Z'}, {'amount': 1, 'price': 1300000, 'time': '2023-01-16T08:55:45Z'}, {'amount': 1, 'price': 1200000, 'time': '2023-01-14T00:23:43Z'}, {'amount': 1, 'price': 1200000, 'time': '2023-01-13T00:44:58Z'}, {'amount': 1, 'price': 1250000, 'time': '2023-01-08T18:32:32Z'}, {'amount': 1, 'price': 999999, 'time': '2023-01-08T11:18:09Z'}, {'amount': 1, 'price': 892500, 'time': '2022-12-31T04:52:07Z'}, {'amount': 1, 'price': 1200000, 'time': '2022-12-29T22:03:25Z'}]}
# histe = HistoryLot(history, search_item_name_by_id("JJd9"))
# histe.create_plot_prices()
# print(search_item_id_by_name("Bee"))
