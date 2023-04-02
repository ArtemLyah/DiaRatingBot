from aiogram.filters import BaseFilter
from aiogram import types
from typing import Union, Collection
from config import ADMINS

class IsAdminFilter(BaseFilter):
    async def __call__(self, message:types.Message):
        return message.from_user.id in ADMINS
    