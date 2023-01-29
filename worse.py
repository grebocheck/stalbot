from datetime import datetime, timezone, timedelta
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
import aiofiles
import os

import database.dbitem as dbitem

from bot import *
from additions.apio import scb


async def get_auc_lot(item_id: str, server: str, lang: str, image_path: str,
                      item_name: str, page: int, order: bool, select: str):
    """
    Функція обробник, формує відповіть з апі в повідомлення для бота
    :param select: Тип сортування
    :param order: По зростанню чи спаданню
    :param item_name: Назва предмету
    :param page: номер сторінки
    :param image_path: Шлях до зображення предмету
    :param item_id: Ідентифікатор предмету (XXXX)
    :param server: Назва серверу
    :param lang: Мова інтерфейсу
    :return: повідомлення
    """
    LEN_TABLE = 5
    limit = LEN_TABLE + 1
    lots = await scb.get_auction_lots(item_id=item_id, region=server, limit=limit,
                                      offset=page * LEN_TABLE, order=order, select=select)
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
    if lang == 'ru':
        img = Image.open('images/pdaRu.png').convert("RGB")
    elif lang == 'uk':
        img = Image.open('images/pdaUa.png').convert("RGB")
    else:
        img = Image.open('images/pdaEn.png').convert("RGB")
    item_image = Image.open(image_path).convert("RGBA").resize((80, 80))
    for iter in range(5):
        img.paste(item_image, (51, 101 + 99 * iter), item_image)
    item_image.close()

    font = ImageFont.truetype("images/Roboto-Medium.ttf", size=25)
    bigFont = ImageFont.truetype("images/Roboto-Medium.ttf", size=30)
    it_artefact = dbitem.is_it_artifact(my_item_id=item_id, server_name=server)
    idraw = ImageDraw.Draw(img)
    for num, lot in enumerate(lots['lots']):
        date = datetime.strptime(lot['endTime'] + "+0000",
                                 "%Y-%m-%dT%H:%M:%SZ%z") - datetime.now(timezone.utc).replace(microsecond=0)
        seconds = round(date.total_seconds())
        hours = round(seconds // 3600)
        minutes = round((seconds - hours * 3600) // 60)
        sec = seconds - hours * 3600 - minutes * 60

        date_str = "%02d:%02d %02d с" % (hours, minutes, sec)

        startPrice = lot['startPrice']
        buyoutPrice = lot['buyoutPrice']

        if buyoutPrice == 0:
            buyoutPrice = "---"

        startPrice_H, startPrice_W = bigFont.getsize(str(startPrice))
        buyoutPrice_H, buyoutPrice_W = bigFont.getsize(str(buyoutPrice))

        quality = 0
        item_name_tab = item_name
        if it_artefact:
            if 'qlt' not in lot['additional'] or lot['additional']['qlt'] == 0:
                quality = 0
            else:
                quality = lot['additional']['qlt']
            if 'ptn' in lot['additional']:
                item_name_tab = f'{item_name} | +{lot["additional"]["ptn"]}'

        quality_color = {
            0: (140, 140, 140),
            1: (0, 200, 50),
            2: (0, 100, 200),
            3: (156, 0, 156),
            4: (200, 0, 0),
            5: (200, 200, 0),
        }

        idraw.text((165, 111 + 99 * num), item_name_tab, font=font, fill=quality_color.get(quality))
        idraw.text((165, 150 + 99 * num), date_str, font=font, fill=(200, 200, 0))

        idraw.text((460 - startPrice_H // 2, 122 + 99 * num), str(startPrice), font=bigFont, fill=(140, 140, 140))
        idraw.text((620 - buyoutPrice_H // 2, 122 + 99 * num), str(buyoutPrice), font=bigFont, fill=(140, 140, 140))
        if num >= 4:
            break
    path = f'table.png'
    img.save(path)
    img.close()
    file = open("table.png", "rb")
    return [file, back_btn, next_btn]


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
