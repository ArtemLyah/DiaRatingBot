from aiogram import Bot, Dispatcher
from databases.db import Database
import config

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
# the storage will save states of users
dp = Dispatcher(bot)

db = Database(
    user="postgres",
    password="postgres",
    database="diarating"
)