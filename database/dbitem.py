import json

with open('database/dbitem/global/listing.json', "rb") as json_file:
    item_db_global = json.load(json_file)

with open('database/dbitem/ru/listing.json', "rb") as json_file:
    item_db_ru = json.load(json_file)


def global_server(serv: str) -> bool:
    """
    Перевірка чи сервер належить до глобальної групи
    :param serv: Назва серверу
    :return: Так чи Ні
    """
    if serv == "RU":
        return False
    else:
        return True


def search_all_gloabal_item_id():
    """
    Пошук всіх ID предметів в глобальній базі данних
    :return: Масив ID предметів глобальних серверів
    """
    mass = []
    for it in item_db_global:
        item_id = it["data"].split("/")[-1][:-5]
        mass.append(item_id)
    return mass


def search_all_ru_item_id() -> list:
    """
    Пошук всіх предметів в ру базі данних
    :return: Масив ID предметів ру сервера
    """
    mass = []
    for it in item_db_ru:
        item_id = it["data"].split("/")[-1][:-5]
        mass.append(item_id)
    return mass


item_id_db_global = search_all_gloabal_item_id()
item_id_db_ru = search_all_ru_item_id()


def search_item_name_by_id(my_item_id: str, server_name: str, lang: str):
    """
    Пошук назви предмета по його ID в базі данних
    :param lang: Мова якою шукається
    :param server_name: Назва серверу
    :param my_item_id: Ідентифікатор предмету (XXXX)
    :return: Назва предмету на EN та RU
    """
    gl_server = global_server(server_name)
    if gl_server:
        for a in item_db_global:
            item_id = a["data"].split("/")[-1][:-5]
            if item_id == my_item_id:
                if lang == 'en':
                    return a["name"]["lines"]["en"]
                else:
                    return a["name"]["lines"]["ru"]
    else:
        for a in item_db_ru:
            item_id = a["data"].split("/")[-1][:-5]
            if item_id == my_item_id:
                if lang == 'en':
                    return a["name"]["lines"]["en"]
                else:
                    return a["name"]["lines"]["ru"]


def search_item_id_by_name(my_item_name: str, server_name: str):
    """
    Пошук Ідентифікатора предмета (XXXX) по його назві в тому числі не повній
    :param server_name: Назва серверу
    :param my_item_name: Назва предмету
    :return: Ідентифікатор предмету (XXXX) або None в випадку якщо предмету немає
    """
    gl_server = global_server(server_name)
    if gl_server:
        for a in item_db_global:
            item_name_ru = a["name"]["lines"]["ru"]
            item_name_en = a["name"]["lines"]["en"]
            if my_item_name.lower() in item_name_ru.lower() or my_item_name.lower() in item_name_en.lower():
                return a["data"].split("/")[-1][:-5]
    else:
        for a in item_db_ru:
            item_name_ru = a["name"]["lines"]["ru"]
            item_name_en = a["name"]["lines"]["en"]
            if my_item_name.lower() in item_name_ru.lower() or my_item_name.lower() in item_name_en.lower():
                return a["data"].split("/")[-1][:-5]
    return None


def get_item_image(my_item_id: str, server_name: str):
    """
    Отримання назви предмету по його ID
    :param my_item_id: Ідентифікатор предмету (XXXX)
    :param server_name: Назва серверу
    :return: Назва предмету
    """
    gl_server = global_server(server_name)
    if gl_server:
        for a in item_db_global:
            item_id = a["data"].split("/")[-1][:-5]
            if item_id == my_item_id:
                return "database/dbitem/global" + a["icon"]
    else:
        for a in item_db_ru:
            item_id = a["data"].split("/")[-1][:-5]
            if item_id == my_item_id:
                return "database/dbitem/ru" + a["icon"]


def is_it_artifact(my_item_id: str, server_name: str):
    """
    Функція перевіряє чи являється цей предмет артефактом
    :param my_item_id: Ідентифікатор предмету (XXXX)
    :param server_name: Назва серверу
    :return: Так чи Ні
    """
    name = get_item_image(my_item_id, server_name)
    status = name.split("/")[3]
    if status == "artefact":
        return True
    else:
        return False
