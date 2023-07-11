from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage
from databases.connection import connectDatabase
from utils.logs import logger
import config

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

db = connectDatabase()
db_session = db.session