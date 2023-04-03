from aiogram import Router, F, filters, types
from aiogram.enums.chat_type import ChatType
from filters import ChatTypeFilter
from data import text

users_router = Router()
users_router.message.filter(ChatTypeFilter(ChatType.PRIVATE))


@users_router.message(filters.CommandStart())
async def start(message:types.Message):
    await message.answer(text.help)

