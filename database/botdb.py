from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DATETIME, Float, String
from sqlalchemy import insert, update, delete
from sqlalchemy.sql import select
from datetime import datetime, timezone, timedelta

bot_engine = create_engine('sqlite:///database/bot/data.db', echo=False)
bot_meta = MetaData()

# Таблиця користувачів
users = Table(
    'users', bot_meta,
    Column('user_id', Integer, primary_key=True),  # Telegram ID користувача
    Column('username', String),  # Юзернейм
    Column('fullname', String),  # Повне ім`я користувача
    Column('lang', String),  # Мова інтерфейсу
    Column('server_name', String),  # Сервер користувача
    Column('born', DATETIME),  # Дата реєстрація в боті
)

# Таблиця підписок на сповіщення
notif = Table(
    'notif', bot_meta,
    Column('user_id', Integer, primary_key=True),  # Telegram ID користувача
    Column('mode', Integer)  # Режим сповіщень
)


def extend_user(user_id: int) -> bool:
    """
    Перевірка чи є користувач в базі
    :param user_id: Telegram ID користувача
    :return: Так чи Ні
    """
    s = select([users]).where(users.c.user_id == user_id)
    conn = bot_engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


def get_user(user_id: int):
    """
    Отримання користувача з бази данних
    :param user_id: Telegram ID користувача
    :return: об`єкт класу User
    """
    s = select([users]).where(users.c.user_id == user_id)
    conn = bot_engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_user = User(user_id=row[0],
                  username=row[1],
                  fullname=row[2],
                  lang=row[3],
                  server_name=row[4],
                  born=row[5])
    return l_user


def get_all_user():
    """
    Отримання всіх користувачів з бази
    :return: масив об`єктів класу User
    """
    s = select([users])
    conn = bot_engine.connect()
    result = conn.execute(s)
    user_mass = []
    for row in result:
        l_user = User(user_id=row[0],
                      username=row[1],
                      fullname=row[2],
                      lang=row[3],
                      server_name=row[4],
                      born=row[5])
        user_mass.append(l_user)
    return user_mass


class User:
    def __init__(self, user_id, username, fullname, lang, server_name, born=datetime.now()):
        """
        Ініціалізація користувача
        :param user_id: Telegram ID користувача
        :param username: Юзернейм
        :param fullname: Ім`я користувача
        :param lang: Мова інтерфейсу
        :param server_name: Сервер користувача
        :param born: Дата реєстрації
        """
        self.user_id = user_id
        self.username = username
        self.fullname = fullname
        self.lang = lang
        self.server_name = server_name
        self.born = born

    def insert_user(self):
        """
        Запис в базу данних
        """
        ins = users.insert().values(user_id=self.user_id,
                                    username=self.username,
                                    fullname=self.fullname,
                                    lang=self.lang,
                                    server_name=self.server_name,
                                    born=self.born)
        conn = bot_engine.connect()
        conn.execute(ins)

    def update_names(self):
        """
        Оновлення імені користувача
        """
        upd = update(users).where(users.c.user_id == self.user_id).values(username=self.username,
                                                                          fullname=self.fullname)
        conn = bot_engine.connect()
        conn.execute(upd)

    def update_lang(self):
        """
        Зміна мови інтерфейсу
        """
        upd = update(users).where(users.c.user_id == self.user_id).values(lang=self.lang)
        conn = bot_engine.connect()
        conn.execute(upd)

    def update_server(self):
        """
        Зміна серверу
        """
        upd = update(users).where(users.c.user_id == self.user_id).values(server_name=self.server_name)
        conn = bot_engine.connect()
        conn.execute(upd)


def extend_notif(user_id: int) -> bool:
    """
    Перевірка на наявність підписки на сповіщення
    :param user_id: Telegram ID користувача
    :return: Так або Ні
    """
    s = select([notif]).where(notif.c.user_id == user_id)
    conn = bot_engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


def get_notif(user_id: int):
    """
    Виведення підписки користувача на сповіщення
    :param user_id: Telegram ID користувача
    :return: об`єкт класу Notif
    """
    s = select([notif]).where(notif.c.user_id == user_id)
    conn = bot_engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_notif = Notif(user_id=row[0], mode=row[1])
    return l_notif


def get_all_notif() -> list:
    """
    Виведення всіх підписок користувачів на сповіщення
    :return: масив об`єктів класу Notif
    """
    s = select([notif])
    conn = bot_engine.connect()
    result = conn.execute(s)
    notif_mass = []
    for row in result:
        l_notif = Notif(user_id=row[0], mode=row[1])
        notif_mass.append(l_notif)
    return notif_mass


def get_all_notif_two_mode() -> list:
    """
    Виведення всіх підписок користувачів на сповіщення що мають другий режим
    :return: масив об`єктів класу Notif
    """
    s = select([notif]).where(notif.c.mode == 2)
    conn = bot_engine.connect()
    result = conn.execute(s)
    notif_mass = []
    for row in result:
        l_notif = Notif(user_id=row[0], mode=row[1])
        notif_mass.append(l_notif)
    return notif_mass


class Notif:
    def __init__(self, user_id, mode):
        """
        Ініціалізація підписок
        :param user_id: Telegram ID користувача
        :param mode: 1 або 2 (без прогнозу викиду або з)
        """
        self.user_id = user_id
        self.mode = mode

    def insert_notif(self):
        """
        Запис в базу даних
        :return:
        """
        ins = notif.insert().values(user_id=self.user_id,
                                    mode=self.mode)
        conn = bot_engine.connect()
        conn.execute(ins)

    def upd_mode(self):
        """
        Оновлення режиму сповіщень
        """
        upd = update(notif).where(notif.c.user_id == self.user_id).values(mode=self.mode)
        conn = bot_engine.connect()
        conn.execute(upd)

    def del_notif(self):
        """
        Видалення з таблиці на сповіщення
        """
        dlf = delete(notif).where(notif.c.user_id == self.user_id)
        conn = bot_engine.connect()
        conn.execute(dlf)


if __name__ == '__main__':
    """
    Ініціює генерацію таблиць бази данних
    """
    bot_meta.create_all(bot_engine)
