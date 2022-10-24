from aiogram.dispatcher import filters
from aiogram import types
from config import father_id

class IsFatherPrivate(filters.BoundFilter):
    async def check(self, message:types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE and message.from_user.id == father_id