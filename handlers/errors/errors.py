from aiogram import Router, types
from aiogram import exceptions
from sqlalchemy.exc import PendingRollbackError, OperationalError
from loader import bot, db_session
from config import ADMINS
from traceback import format_exc
from utils.logs import logger
from asyncio import sleep
import os

error_router = Router()

@error_router.errors()
async def error_handler(event: types.ErrorEvent):
    if isinstance(event.exception, exceptions.TelegramBadRequest):
        logger.debug("TelegramBadRequest")
    if isinstance(event.exception, (PendingRollbackError, OperationalError)):
        os.system('sudo service postgresql restart')
        await sleep(1)
        db_session.rollback()

    logger.exception(format_exc())
    await bot.send_message(ADMINS[0], format_exc(limit=-5, chain=False))
    return True