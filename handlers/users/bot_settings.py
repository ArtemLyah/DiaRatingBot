from aiogram import filters, types
from dispatcher import dp
from databases import stickers
from filters import IsPrivate, IsFather
from state import AddSticker_State
from aiogram.dispatcher.storage import FSMContext
from logs import logger

# handle private messages
@dp.message_handler(filters.CommandStart(), IsPrivate(), IsFather())
async def start(message:types.Message):
    await message.answer("OK")
    await message.answer(message)

@dp.message_handler(IsPrivate(), IsFather(), filters.Command("add_sticker"))
async def set_sticker(message:types.Message):
    await message.answer("Send sticker here")
    await AddSticker_State.add_sticker.set()

@dp.message_handler(IsPrivate(), IsFather(), 
    content_types=types.ContentTypes.STICKER, 
    state=AddSticker_State.add_sticker)
async def add_sticker(message:types.Message, state:FSMContext):
    await state.update_data({
        "unique_file_id" : message.sticker.thumb.file_unique_id
    })
    await message.answer("Now send rate of the sticker")
    await AddSticker_State.add_rate.set()
@dp.message_handler(IsPrivate(), IsFather(), state=AddSticker_State.add_rate)
async def add_rate(message:types.Message, state:FSMContext):
    unique_file_id = (await state.get_data())["unique_file_id"]
    rating = int(message.text)
    stickers.add_sticker(unique_file_id, rating)
    logger.info(f"New sticker <unique_file_id={unique_file_id}, rating={rating}>")
    await message.answer(f"New sticker <unique_file_id={unique_file_id}, rating={rating}> has been added")
    await state.finish()
    