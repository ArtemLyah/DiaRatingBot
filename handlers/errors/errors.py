from dispatcher import dp, db
from aiogram import types
from aiogram.utils import exceptions
from psycopg2 import InterfaceError
import logging

@dp.errors_handler()
async def error_handler(update:types.Update, exception):
    if isinstance(exception, InterfaceError):
        db.reload()
    else:
        logging.debug(exception)
    return True