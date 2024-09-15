from datetime import datetime, timezone, timedelta
from prettytable import PrettyTable
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
import aiofiles
import os
import re

import database.dbitem as dbitem

from bot import *
from additions.apio import scb

matplotlib.use('Agg')


async def get_auc_lot(item_id: str, server: str, lang: str, image_path: str,
                      item_name: str, page: int, order: bool, select: str, user_id):
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
    if lots.get('total') == 0:
        return [None, False, False]

    if 'lots' not in lots:
        page = 0
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
    smallFont = ImageFont.truetype("images/Roboto-Medium.ttf", size=14)
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

        if 'currentPrice' in lot:
            startPrice = lot['currentPrice']
        else:
            startPrice = lot['startPrice']
        buyoutPrice = lot['buyoutPrice']
        amount = lot['amount']

        if buyoutPrice == 0:
            buyoutPrice = "---"

        startPrice_H, startPrice_W = bigFont.getsize(str(startPrice))
        buyoutPrice_H, buyoutPrice_W = bigFont.getsize(str(buyoutPrice))

        quality = 0
        item_name_tab = re.sub(r'^(.{15}).*$', '\g<1>...', item_name)
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
        if amount > 1:
            idraw.text((70, 163 + 99 * num), f"{amount} шт.", font=font, fill=(255, 255, 255))

        idraw.text((460 - startPrice_H // 2, 125 + 99 * num), str(startPrice), font=bigFont, fill=(140, 140, 140))
        idraw.text((620 - buyoutPrice_H // 2, 125 + 99 * num), str(buyoutPrice), font=bigFont, fill=(140, 140, 140))

        if num >= 4:
            break
    idraw.text((80, 592), server, font=smallFont, fill=(140, 140, 140))
    path = f'table{user_id}.png'
    img.save(path)
    img.close()
    return [path, back_btn, next_btn]


async def get_history(item_id: str, server: str, lang: str, item_name: str, image_path: str, days_lim=None):
    """
    Функція обробник, на основі запиту на історію формує графік
    :param days_lim: До какого времени собирать график
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
    max_iterations = 1000
    if days_lim is None:
        days_lim = 10000
    lim_time = datetime.now(timezone.utc) - timedelta(days=days_lim)
    if not histo_prices:
        return ['images/not-found.png']
    for a in range(max_iterations):
        last_time = datetime.strptime(histo['prices'][-1]['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")
        len_histo = len(histo['prices'])
        if last_time < lim_time or len_histo != 100:
            break
        else:
            histo = await scb.get_auction_history(item_id=item_id, region=server, limit=100, offset=k * 99)
            k += 1
            if 'prices' in histo:
                histo_prices += histo['prices'][1:]
            else:
                break

    histo_filt = []
    for a in histo_prices:
        a_time = datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")
        if a_time > lim_time:
            histo_filt.append(a)

    cords = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}
    for a in histo_filt:
        if 'qlt' not in a['additional'] or a['additional']['qlt'] == 0:
            cords['0'].append([int(a['price'])/int(a['amount']), datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")])
        elif a['additional']['qlt'] == 1:
            cords['1'].append([int(a['price'])/int(a['amount']), datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")])
        elif a['additional']['qlt'] == 2:
            cords['2'].append([int(a['price'])/int(a['amount']), datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")])
        elif a['additional']['qlt'] == 3:
            cords['3'].append([int(a['price'])/int(a['amount']), datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")])
        elif a['additional']['qlt'] == 4:
            cords['4'].append([int(a['price'])/int(a['amount']), datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")])
        elif a['additional']['qlt'] == 5:
            cords['5'].append([int(a['price'])/int(a['amount']), datetime.strptime(a['time'] + "+0000", "%Y-%m-%dT%H:%M:%SZ%z")])
    mass_images = []
    colors = {"0": "gray", "1": "green", "2": "blue", "3": "purple", "4": "red", "5": "yellow"}
    qlt = {
        'uk': {"0": "Звичайний", "1": "Незвичайний", "2": "Особливий", "3": "Рідкісний",
               "4": "Виключний", "5": "Легендарний"},
        'en': {"0": "Normal", "1": "Unusual", "2": "Special", "3": "Rare",
               "4": "Exceptional", "5": "Legendary"},
        'ru': {"0": "Обычный", "1": "Необычный", "2": "Особый", "3": "Редкий",
               "4": "Исключительный", "5": "Легендарный"},
    }
    for a in cords:
        # plt.semilogy()
        mass_pl = {}
        for b in cords[a]:
            greph_time = datetime(year=b[1].year,
                                  month=b[1].month,
                                  day=b[1].day)
            if greph_time not in mass_pl:
                mass_pl[greph_time] = [b[0], b[0]]
            else:
                elem = mass_pl[greph_time]
                if elem[0] > b[0]:
                    mass_pl[greph_time] = [b[0], elem[1]]
                elif elem[1] < b[0]:
                    mass_pl[greph_time] = [elem[0], b[0]]

        if not mass_pl:
            continue

        mass_min_y = []
        mass_max_y = []
        mass_x = []
        for c in mass_pl:
            mass_x.append(c)
            mass_max_y.append(mass_pl[c][1])
            mass_min_y.append(mass_pl[c][0])
        f_color = '#6E7F80'
        text_color = 'white'
        plt.figure(figsize=(10, 10), facecolor=f_color, edgecolor=text_color)
        ax = plt.axes()
        ax.set_facecolor(f_color)
        ax.tick_params(labelcolor=text_color, labelsize=16)

        def formatPrice(price, x):
            price = round(price)
            sprice = str(price)
            ks = (len(sprice) - 1) // 3
            if ks == 0:
                return sprice
            else:
                s = ''
                if sprice[-(ks * 3):-(ks * 3) + 1] != '0':
                    s = ',' + sprice[-(ks * 3):-(ks * 3) + 1]
                    if sprice[-(ks * 3) + 1:-(ks * 3) + 2] != '0':
                        s += sprice[-(ks * 3) + 1:-(ks * 3) + 2]
                prc = sprice[0:-(ks * 3)] + s + 'k' * ks
                return prc

        ax.yaxis.set_major_formatter(FuncFormatter(formatPrice))
        for spn in ax.spines.values(): spn.set_color('black')
        for t in ax.xaxis.get_ticklines(): t.set_color(text_color)
        for t in ax.yaxis.get_ticklines(): t.set_color(text_color)
        plt.plot(mass_x, mass_min_y, color='black', linewidth=2, marker='o', markerfacecolor='black', markersize=3)
        plt.plot(mass_x, mass_max_y, color='black', linewidth=2, marker='o', markerfacecolor='black', markersize=3)
        plt.fill_between(mass_x, mass_min_y, mass_max_y,
                         facecolor=colors[a])
        plt.xticks(rotation=20)
        it_artefact = dbitem.is_it_artifact(my_item_id=item_id, server_name=server)
        if lang == "en":
            xlab = plt.xlabel('Time')
            ylab = plt.ylabel('Price, rub')
            if it_artefact:
                title = plt.title(f'{item_name} {server} ({qlt[lang][a]})')
            else:
                title = plt.title(f'{item_name} {server}')
        elif lang == "uk":
            xlab = plt.xlabel('Час')
            ylab = plt.ylabel('Ціна, руб')
            if it_artefact:
                title = plt.title(f'{item_name} {server} ({qlt[lang][a]})')
            else:
                title = plt.title(f'{item_name} {server}')
        else:
            xlab = plt.xlabel('Время')
            ylab = plt.ylabel('Цена, руб')
            if it_artefact:
                title = plt.title(f'{item_name} {server} ({qlt[lang][a]})')
            else:
                title = plt.title(f'{item_name} {server}')
        xlab.set_color(text_color)
        ylab.set_color(text_color)
        title.set_color(text_color)
        f_size = 15
        xlab.set_fontsize(f_size)
        ylab.set_fontsize(f_size)
        title.set_fontsize(25)
        ax = plt.gca()
        im = plt.imread(image_path)
        ax.figure.figimage(im,
                           im.shape[0],  # ax.bbox.xmax // 1 - im.shape[0] // 1,
                           ax.bbox.ymax // 1 - im.shape[1] // 1,
                           alpha=1, zorder=1)
        f_name = f"plots/plot{a}.png"
        plt.savefig(f_name)
        plt.close()
        mass_images.append(f_name)
    if not mass_images:
        mass_images.append('images/not-found.png')
    return mass_images
