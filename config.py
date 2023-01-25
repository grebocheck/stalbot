import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

client_id = config['StalCraft']['client_id']
client_secret = config['StalCraft']['client_secret']
telegram_token = config['Telegram']['token']