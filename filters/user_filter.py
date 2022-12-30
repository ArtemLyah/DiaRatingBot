from aiogram.dispatcher import filters
from aiogram import types
from config import FATHER_ID

class IsPrivate(filters.BoundFilter):
    async def check(self, message:types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE

class IsFather(filters.BoundFilter):
    async def check(self, message:types.Message) -> bool:
        return message.from_user.id == FATHER_ID