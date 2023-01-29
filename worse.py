from datetime import datetime, timezone, timedelta
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
import aiofiles
import os

import database.dbitem as dbitem

from bot import *
from additions.apio import scb


async def get_auc_lot(item_id: str, server: str, lang: str, image_path: str, page: int):
    """
    Функція обробник, формує відповіть з апі в повідомлення для бота
    :param image_path: Назва предмету
    :param item_id: Ідентифікатор предмету (XXXX)
    :param server: Назва серверу
    :param lang: Мова інтерфейсу
    :return: повідомлення
    """
    LEN_TABLE = 20
    limit = LEN_TABLE + 1
    lots = await scb.get_auction_lots(item_id=item_id, region=server, limit=limit, offset=page*LEN_TABLE)
    if len(lots['lots']) == limit:
        next_btn = True
    else:
        next_btn = False
    if page == 0:
        back_btn = False
    else:
        back_btn = True
    if lots.get('total') == 0:
        return [None, False, False]
    mass = []
    it_artefact = dbitem.is_it_artifact(my_item_id=item_id, server_name=server)
    for a in lots['lots']:
        date = datetime.strptime(a['endTime'] + "+0000",
                                 "%Y-%m-%dT%H:%M:%SZ%z") - datetime.now(timezone.utc).replace(microsecond=0)
        hours = round(date.total_seconds() / 3600)
        minutes = round(date.total_seconds() % 60)
        date_str = "%02dh:%02dm" % (hours, minutes)
        row = [a['startPrice'], a['buyoutPrice'], date_str]
        if it_artefact:
            if 'qlt' not in a['additional'] or a['additional']['qlt'] == 0:
                quality = 0
            else:
                quality = a['additional']['qlt']
            row.append(quality)
        mass.append(row)
    if lang == "en":
        field_names = ["Start price", "Out price", "Time"]
        if it_artefact:
            field_names.append("Qlt.")
    elif lang == "uk":
        field_names = ["Початкова ціна", "Викуп", "Час"]
        if it_artefact:
            field_names.append("Рідк.")
    else:
        field_names = ["Ставка", "Выкуп", "Время"]
        if it_artefact:
            field_names.append("Ред.")
    fig, axs = plt.subplots()
    fig.patch.set_visible(False)
    axs.axis('tight')
    axs.axis('off')
    fig.tight_layout()
    axs.table(cellText=mass, colLabels=field_names, loc='center')
    ax = plt.gca()
    im = plt.imread(image_path)
    ax.figure.figimage(im,
                       ax.bbox.xmax // 2 - im.shape[0] // 2,
                       ax.bbox.ymax // 2 - im.shape[1] // 2,
                       alpha=.50, zorder=1)
    plt.savefig("table.png")
    plt.close()
    img = open("table.png", "rb")
    return [img, back_btn, next_btn]


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
    histo = await scb.get_auction_history(item_id=item_id, region=server, limit=100, offset=0)
    histo_prices = histo['prices']
    k = 1
    while True:
        last_time = datetime.strptime(histo['prices'][-1]['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")
        len_histo = len(histo['prices'])
        if last_time < datetime.now(timezone.utc) - timedelta(days=30) or len_histo != 100:
            break
        else:
            histo = await scb.get_auction_history(item_id=item_id, region=server, limit=100, offset=k * 99)
            k += 1
            histo_prices += histo['prices'][1:]
    y = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}
    x = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}
    for a in histo_prices:
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
    plt.figure(figsize=(10, 10))
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
    if lang == "en":
        plt.xlabel('Time')
        plt.ylabel('Price, rub')
        plt.title(f'Price of {item_name} on server {server}')
    elif lang == "uk":
        plt.xlabel('Час')
        plt.ylabel('Ціна, руб')
        plt.title(f'Ціна на {item_name} на сервері {server}')
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
