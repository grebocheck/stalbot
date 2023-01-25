import api_sc

from datetime import datetime, timezone, timedelta
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import aiofiles
import os

import dbitem

scb = api_sc.StalcraftAPI()


async def get_auc_lot(item_id: str, server: str, lang: str):
    """
    Функція обробник, формує відповіть з апі в повідомлення для бота
    :param item_id: Ідентифікатор предмету (XXXX)
    :param server: Назва серверу
    :param lang: Мова інтерфейсу
    :return: повідомлення
    """
    lots = await scb.get_auction_lots(item=item_id, region=server)
    mass = []
    it_artefact = dbitem.is_it_artifact(my_item_id=item_id, server_name=server)
    for a in lots['lots']:
        date = datetime.strptime(a['endTime'] + "+0000",
                                 "%Y-%m-%dT%H:%M:%SZ%z") - datetime.now(timezone.utc).replace(microsecond=0)
        hours = round(date.total_seconds() / 3600)
        minutes = round(date.total_seconds() % 60)
        date_str = "%d:%d" % (hours, minutes)
        row = [a['startPrice'], a['buyoutPrice'], date_str]
        if it_artefact:
            if 'qlt' not in a['additional'] or a['additional']['qlt'] == 0:
                quality = 0
            else:
                quality = a['additional']['qlt']
            row.append(quality)
        mass.append(row)
    tab = PrettyTable()
    if lang == "EN":
        field_names = ["Start price", "Out price", "Time"]
        if it_artefact:
            field_names.append("Qlt.")
        tab.field_names = field_names
    else:
        field_names = ["Ставка", "Выкуп", "Время"]
        if it_artefact:
            field_names.append("Ред.")
        tab.field_names = field_names
    for a in mass:
        tab.add_row(a)
    return tab.get_string()


async def get_history(item_id: str, server: str, lang: str, item_name: str, image_path: str):
    """
    Функція обробник, на основі запиту на історію формує графік
    :param item_id: Ідентифікатор предмету (XXXX)
    :param server: Назва серверу
    :param lang: Мова інтерфейсу
    :param item_name: Назва предмету
    :param image_path: Шлях до зображення предмету
    :return: Графік в вигляді зображення
    """
    histo = await scb.get_price_history(item=item_id, region=server)
    y = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}
    x = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}
    for a in histo['prices']:
        if 'qlt' not in a['additional'] or a['additional']['qlt'] == 0:
            y['0'].append(a['price'])
            x['0'].append(datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
        elif a['additional']['qlt'] == 1:
            y['1'].append(a['price'])
            x['1'].append(datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
        elif a['additional']['qlt'] == 2:
            y['2'].append(a['price'])
            x['2'].append(datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
        elif a['additional']['qlt'] == 3:
            y['3'].append(a['price'])
            x['3'].append(datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
        elif a['additional']['qlt'] == 4:
            y['4'].append(a['price'])
            x['4'].append(datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
        elif a['additional']['qlt'] == 5:
            y['5'].append(a['price'])
            x['5'].append(datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
        elif a['additional']['qlt'] == 6:
            y['6'].append(a['price'])
            x['6'].append(datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z"))
    plt.plot(x['0'], y['0'], color="gray", marker='o', markerfacecolor='black', markersize=3, label='0')
    plt.plot(x['1'], y['1'], color="green", marker='o', markerfacecolor='black', markersize=3, label='1')
    plt.plot(x['2'], y['2'], color="blue", marker='o', markerfacecolor='black', markersize=3, label='2')
    plt.plot(x['3'], y['3'], color="purple", marker='o', markerfacecolor='black', markersize=3, label='3')
    plt.plot(x['4'], y['4'], color="red", marker='o', markerfacecolor='black', markersize=3, label='4')
    plt.plot(x['5'], y['5'], color="yellow", marker='o', markerfacecolor='black', markersize=3, label='5')
    plt.plot(x['6'], y['6'], color="magenta", marker='o', markerfacecolor='black', markersize=3, label='6')
    plt.legend()
    plt.semilogy()
    plt.xticks(rotation=20)
    if lang == "EN":
        plt.xlabel('Time')
        plt.ylabel('Price, rub')
        plt.title(f'Price of {item_name} on server {server}')
    else:
        plt.xlabel('Время')
        plt.ylabel('Цена, руб')
        plt.title(f'Цены на {item_name} на сервере {server}')
    ax = plt.gca()
    im = plt.imread(image_path)
    ax.figure.figimage(im,
                       ax.bbox.xmax // 2 - im.shape[0] // 2,
                       ax.bbox.ymax // 2 - im.shape[1] // 2,
                       alpha=.50, zorder=1)

    plt.savefig("plot.png")
    plt.close()
    async with aiofiles.open("plot.png", "rb") as f:
        img = await f.read()
    os.remove("plot.png")
    return img
