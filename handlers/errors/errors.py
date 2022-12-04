from dispatcher import dp, bot
from databases import database
from aiogram import types
from aiogram.utils.exceptions import RetryAfter
from psycopg2 import InterfaceError
from config import father_id
from logs import logger

@dp.errors_handler()
async def error_handler(update:types.Update, exception:Exception):
    if isinstance(exception, InterfaceError):
        await bot.send_message(father_id, "Reconnecting...")
        logger.exception("[InterfaceError] Database reconecting...")
        database.connect()
        await bot.send_message(father_id, "Reconnecting has done")
        logger.info("[InterfaceError] Database has been reconected!")
    elif isinstance(exception, RetryAfter):
        logger.warning(exception)
    else:
        await bot.send_message(father_id, str(exception))
        logger.exception(exception)
    await update.message.answer("😢Бот трошки поламався😢\n🛠Зараз криворукий розробник все налагодить🛠")
    return True