from aiogram import Bot, Dispatcher
from databases.db import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
# the storage will save states of users
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


db = Database(
    user="postgres",
    password="postgres",
    database="diarating"
)