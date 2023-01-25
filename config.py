import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

client_id = config['stalcraft']['client_id']
client_secret = config['stalcraft']['client_secret']
telegram_token = config['stalcraft']['telegram_token']