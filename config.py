import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

#stalcraft
client_id = config['StalCraft']['client_id']
client_secret = config['StalCraft']['client_secret']

#telegram
telegram_token = config['Telegram']['token']

#mongo
mongoConnectUrl = config['MongoDB']['connection_url']
mongoDataBase = config['MongoDB']['dataBase']
mongoStorageBase = config['MongoDB']['storageBase']

available_languages = ['ru', 'en', 'uk']