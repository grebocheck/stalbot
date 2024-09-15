import os, time

from aiogram.contrib.fsm_storage.mongo import MongoStorage

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, BotCommand, \
    ChatActions, video_note, ContentType
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiogram.utils.exceptions

from aiogram import filters as ft

import database.dbitem as dbitem
import config
from additions.log import log_deb, log_err, log_inf
import database.botdb as botdb
import worse
from additions.database import db
from additions.user_data import get_user_server, get_user_emission, get_all_users_emission, get_all_users

from additions.language import Language

from forms import *

lng = Language()

bot = Bot(token=str(config.telegram_token), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MongoStorage(uri=config.mongoConnectUrl, db_name=config.mongoStorageBase))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Updates were skipped successfully.')
    return