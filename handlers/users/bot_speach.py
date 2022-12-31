from aiogram import filters, types
from dispatcher import dp, bot
from filters import IsPrivate, IsFather
from logs import logger

@dp.message_handler(IsPrivate(), IsFather())
async def get_message(message:types.Message):
    chat_id = -1001747851953
    await bot.send_message(chat_id, message.text)