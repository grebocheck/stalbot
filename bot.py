import os, time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, BotCommand, \
    ChatActions, video_note, ContentType
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiogram.utils.exceptions

import database.dbitem as dbitem
import config
import language.texts as texts
from additions.log import log_deb, log_err, log_inf
import database.botdb as botdb
import worse

import additions.stalApi as stalApi

from forms import *
from keyboards import *

scb = stalApi.StalcraftAPI(client_id=config.client_id, client_secret=config.client_secret)

bot = Bot(token=str(config.telegram_token), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Updates were skipped successfully.')
    return