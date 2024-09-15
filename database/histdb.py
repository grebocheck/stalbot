from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DATETIME, Float
from sqlalchemy import insert
from sqlalchemy.sql import select
from datetime import datetime, timezone, timedelta
from database.dbitem import item_id_db_global, item_id_db_ru

"""
Файл для вводу та виведення інформації про історію цін
"""

EU_engine = create_engine('sqlite:///database/history/EU_histo.db', echo=False)
EU_meta = MetaData()
RU_engine = create_engine('sqlite:///database/history/RU_histo.db', echo=False)
RU_meta = MetaData()
NA_engine = create_engine('sqlite:///database/history/NA_histo.db', echo=False)
NA_meta = MetaData()
SEA_engine = create_engine('sqlite:///database/history/SEA_histo.db', echo=False)
SEA_meta = MetaData()


table_names_global = item_id_db_global
table_names_ru = item_id_db_ru

EU_tables = {}
RU_tables = {}
NA_tables = {}
SEA_tables = {}

# Побудова таблиць
for a in table_names_global:
    b = Table(
        a, EU_meta,
        Column('price', Float),
        Column('amount', Integer),
        Column('date', DATETIME)
    )
    c = Table(
        a, NA_meta,
        Column('price', Float),
        Column('amount', Integer),
        Column('date', DATETIME)
    )
    d = Table(
        a, SEA_meta,
        Column('price', Float),
        Column('amount', Integer),
        Column('date', DATETIME)
    )
    EU_tables[a] = b
    NA_tables[a] = c
    SEA_tables[a] = d

for a in table_names_ru:
    b = Table(
        a, RU_meta,
        Column('price', Float),
        Column('amount', Integer),
        Column('date', DATETIME)
    )
    RU_tables[a] = b


def extend_row(server: str, item_id: str, date: datetime) -> bool:
    """
    Перевірка на те чи є запис в базі данних
    :param server: Назва серверу
    :param item_id: Ідентифікатор предмету (XXXX)
    :param date: Дата та час
    :return: Чи існує предмет?
    """
    if server == "EU":
        sel = select(EU_tables[item_id]).where(EU_tables[item_id].c.date == date)
        conn = EU_engine.connect()
    elif server == "RU":
        sel = select(RU_tables[item_id]).where(RU_tables[item_id].c.date == date)
        conn = RU_engine.connect()
    elif server == "NA":
        sel = select(NA_tables[item_id]).where(NA_tables[item_id].c.date == date)
        conn = NA_engine.connect()
    else:
        sel = select(SEA_tables[item_id]).where(SEA_tables[item_id].c.date == date)
        conn = SEA_engine.connect()
    result = conn.execute(sel)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


def insert_hist(server: str, item_id: str, amount: int, price: float, date: datetime):
    """
    Створення запису історії в базі данних
    :param server: Назва серверу
    :param item_id: Ідентифікатор предмету (XXXX)
    :param amount: Кількість
    :param price: Ціна
    :param date: Дата та час
    :return: Нічого
    """
    if server == "EU":
        ins = insert(EU_tables[item_id]).values(amount=amount, price=price, date=date)
        conn = EU_engine.connect()
    elif server == "RU":
        ins = insert(RU_tables[item_id]).values(amount=amount, price=price, date=date)
        conn = RU_engine.connect()
    elif server == "NA":
        ins = insert(NA_tables[item_id]).values(amount=amount, price=price, date=date)
        conn = NA_engine.connect()
    else:
        ins = insert(SEA_tables[item_id]).values(amount=amount, price=price, date=date)
        conn = SEA_engine.connect()
    conn.execute(ins)


def select_hist_month(server: str, item_id: str):
    """
    Запит на отримання історії цін предмету за останній місяць
    :param server: Назва серверу
    :param item_id: Ідентифікатор предмету (XXXX)
    :return: Масив з історією
    """
    month_ago = datetime.now(tz=timezone.utc) - timedelta(days=30)
    if server == "EU":
        sel = select(EU_tables[item_id]).where(EU_tables[item_id].c.date > month_ago)
        conn = EU_engine.connect()
    elif server == "RU":
        sel = select(RU_tables[item_id]).where(RU_tables[item_id].c.date > month_ago)
        conn = RU_engine.connect()
    elif server == "NA":
        sel = select(NA_tables[item_id]).where(NA_tables[item_id].c.date > month_ago)
        conn = NA_engine.connect()
    else:
        sel = select(SEA_tables[item_id]).where(SEA_tables[item_id].c.date > month_ago)
        conn = SEA_engine.connect()
    result = conn.execute(sel)
    return result


if __name__ == '__main__':
    """
    Ініціює генерацію таблиць бази данних
    """
    EU_meta.create_all(EU_engine)
    RU_meta.create_all(RU_engine)
    NA_meta.create_all(NA_engine)
    SEA_meta.create_all(SEA_engine)
