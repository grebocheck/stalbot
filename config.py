import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

#stalcraft
client_id = config['StalCraft']['client_id']
client_secret = config['StalCraft']['client_secret']
repo_dir = config['StalCraft']['repo_dir']
repo_url = config['StalCraft']['repo_url']

#telegram
telegram_token = config['Telegram']['token']
admin_list = [int(item) for item in config['Telegram']['admins'].split(" ")]

#mongo
mongoConnectUrl = config['MongoDB']['connection_url']
mongoDataBase = config['MongoDB']['dataBase']
mongoStorageBase = config['MongoDB']['storageBase']

available_languages = ['ru', 'en', 'uk']