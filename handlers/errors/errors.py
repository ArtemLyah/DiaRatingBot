from aiogram import Router, types
from aiogram import exceptions
from sqlalchemy.exc import PendingRollbackError
from loader import bot, db_session
from config import ADMINS
from traceback import format_exc
import logging

error_router = Router()

@error_router.errors()
async def error_handler(event: types.ErrorEvent):
    if isinstance(event.exception, exceptions.TelegramBadRequest):
        logging.debug("Bot was blocked")
    if isinstance(event.exception, PendingRollbackError):
        db_session.rollback()
    logging.exception(format_exc())
    await bot.send_message(ADMINS[0], format_exc(limit=-5, chain=False))
    return True