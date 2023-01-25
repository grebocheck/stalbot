from aiogram.dispatcher.filters.state import State, StatesGroup

# форма реєстрації
class Form_Reg(StatesGroup):
    get_lang = State()
    get_serv = State()


# форма зміни мови інтерфейсу
class Form_Lang(StatesGroup):
    get_lang = State()


# форма зміни серверу
class Form_Serv(StatesGroup):
    get_serv = State()


# форма отримання історії цін на предмет
class Form_Hist(StatesGroup):
    get_item = State()


# форма отримання цін на предмет на аукціоні
class Form_Check(StatesGroup):
    get_item = State()


# форма налаштуваннь сповіщень про викиди
class Form_Notif(StatesGroup):
    get_mode = State()