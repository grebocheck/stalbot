from additions.database import db
from aiogram.types import User


async def get_user_server(user):
    # get user language preferebly from database, otherwise from telegram user settings
    region = "RU"
    bd_data = await db.userSettings.find_one({'telegram_id': user.id})  # get language user language from database
    if bd_data and bd_data.get('region'):  # if user in database
        return bd_data.get('region')
    else:
        return region


async def get_user_emission(user):
    emission_default = False
    bd_data = await db.userSettings.find_one({'telegram_id': user.id})
    if bd_data and bd_data.get('emission'):
        return bd_data.get('emission')
    else:
        return emission_default


async def get_all_users_emission():
    bd_data = db.userSettings.find({'emission': True})
    mass = []
    async for a in bd_data:
        user = User()
        user.id = a.get('telegram_id')
        mass.append(user)
    return mass
