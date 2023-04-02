from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage
from databases.connection import Database
from databases.models import *
from utils.logs import logger

import config

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

db = Database(config.db_settings)
db.connect()
db_session = db.session
logger.debug("Connenced to database")

if config.create_db:
    db.Base.metadata.create_all(db.engine)
    logger.debug("Create tables in database")
