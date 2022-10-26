from aiogram.dispatcher import filters
from aiogram import types
from dispatcher import db
# creating filters we must to create a method check
# this method will be check a message on a certain condition
# BoundFilter - main class of filters
# result must be Boolean
class IsGroup(filters.BoundFilter):
    async def check(self, message:types.Message) -> bool:
        return message.chat.type == types.ChatType.GROUP or message.chat.type == types.ChatType.SUPERGROUP

class IsReplyDiaStickers(filters.BoundFilter):
    async def check(self, message:types.Message) -> bool:
        return message.reply_to_message and db.status_info.get_rate(message.sticker.thumb.file_unique_id)