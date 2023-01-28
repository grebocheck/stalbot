from additions.database import db


async def get_user_server(user):
    # get user language preferebly from database, otherwise from telegram user settings
    region = "RU"
    bd_data = await db.userSettings.find_one({'telegram_id': user.id})  # get language user language from database
    if bd_data and bd_data.get('region'):  # if user in database
        return bd_data.get('region')
    else:
        return region


async def get_user_emission(user):
    # get user language preferebly from database, otherwise from telegram user settings
    emission_default = False
    bd_data = await db.userSettings.find_one({'telegram_id': user.id})  # get language user language from database
    if bd_data and bd_data.get('emission'):  # if user in database
        return bd_data.get('emission')
    else:
        return emission_default
