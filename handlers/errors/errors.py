from dispatcher import dp, bot
from databases import database
from aiogram import types
from aiogram.utils.exceptions import RetryAfter, TerminatedByOtherGetUpdates
from psycopg2 import InterfaceError
from config import FATHER_ID
from logs import logger

@dp.errors_handler()
async def error_handler(update:types.Update, exception:Exception):
    if isinstance(exception, InterfaceError):
        await bot.send_message(FATHER_ID, "Reconnecting...")
        logger.exception("[InterfaceError] Database reconecting...")
        database.connect()
        await bot.send_message(FATHER_ID, "Reconnecting has done")
        logger.info("[InterfaceError] Database has been reconected!")
    elif isinstance(exception, RetryAfter):
        logger.warning(exception)
    else:
        await bot.send_message(FATHER_ID, str(exception))
        logger.error("=============================================================")
        logger.exception(exception)
        logger.exception("Message information"
            "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"+\
            f"<Chat id: {update.message.chat.id}>\n<From user id: {update.message.from_user.id}>"+\
            "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
        await update.message.answer("😢Бот трошки поламався😢\n🛠Зараз криворукий розробник все налагодить🛠")
    return True