from aiogram import types, filters
from dispatcher import dp
from filters import IsGroup
from databases import groups
from logs import logger
from utils.message_text import help_text

@dp.message_handler(filters.CommandStart(), IsGroup())
async def start(message:types.Message):
    await message.answer(help_text)
    groups.add(message.chat.id, message.chat.username, message.chat.full_name)
    logger.info(f"New start in group <id={message.chat.id}, name={message.chat.full_name}>")

@dp.message_handler(filters.Command(["help"]), IsGroup())
async def help(message:types.Message):
    await message.answer(help_text)