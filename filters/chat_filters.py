from aiogram.filters import BaseFilter
from aiogram import types
from typing import Union, Collection

class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: Union[str, Collection]) -> None:
        self.chat_type = chat_type
    async def __call__(self, message:types.Message):
        if isinstance(self.chat_type, Collection):
            return message.chat.type in self.chat_type
        return message.chat.type == self.chat_type 
    