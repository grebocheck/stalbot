from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.message import Message

from bot import lng


class transFilter(BoundFilter):
    def __init__(self, textToTranslate):
        self.text_to_translate = textToTranslate

    async def check(self, msg: Message):
        user = msg.from_user
        text = await lng.trans(self.text_to_translate, user)
        if text:
            return True
        else:
            return False
            