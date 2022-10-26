from dispatcher import dp, db, bot
from aiogram import types
from psycopg2 import InterfaceError
from config import father_id
import logging

@dp.errors_handler()
async def error_handler(update:types.Update, exception:Exception):
    if isinstance(exception, InterfaceError):
        db.connect()
    else:
        await bot.send_message(father_id, str(exception))
        logging.exception(str(exception))
    return True