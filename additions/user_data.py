from additions.database import db


async def get_user_server(user):
    # get user language preferebly from database, otherwise from telegram user settings
    region = "RU"
    bd_region = await db.userSettings.find_one({'telegram_id': user.id})  # get language user language from database
    if bd_region and bd_region.get('region'):  # if user in database
        return bd_region.get('region')
    else:
        return region
