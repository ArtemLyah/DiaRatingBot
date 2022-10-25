from aiogram import filters, types
from dispatcher import dp
from filters import IsFatherPrivate

# handle private messages
@dp.message_handler(filters.CommandStart(), IsFatherPrivate())
async def start(message:types.Message):
    await message.answer("OK")
    await message.answer(message)

@dp.message_handler(IsFatherPrivate(), content_types=types.ContentTypes.STICKER)
async def get_sticker_id(message:types.Message):
    await message.answer(message.sticker.thumb.file_unique_id)