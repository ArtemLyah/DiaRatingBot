from dispatcher import dp, db, bot
from aiogram import types
from psycopg2 import InterfaceError
from config import father_id
import logging

@dp.errors_handler()
async def error_handler(update:types.Update, exception:Exception):
    if isinstance(exception, InterfaceError):
        await bot.send_message(father_id, "Reconnecting...")
        db.connect()
        await bot.send_message(father_id, "Reconnecting has done")
    else:
        await bot.send_message(father_id, str(exception))
        logging.exception(exception)
    await update.message.answer("😢Бот трошки поламався😢\n🛠Зараз криворукий розробник все налагодить🛠")
    await update.message.answer_sticker("CAACAgUAAxkBAAIOdmNhXMBPxA0kdXThud37MLTRGK6AAAKpBAAC-nCQVAQILB5AKITMKgQ")
    return True