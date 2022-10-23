from dispatcher import dp
from aiogram import types
from aiogram.utils import exceptions
import logging

@dp.errors_handler()
async def error_handler(update:types.Update, exception):
    if isinstance(exception, exceptions.BotBlocked):
        logging.debug("Bot was blocked")
    return True