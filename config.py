from dotenv import load_dotenv
from aiogram.utils.markdown import hlink
import os

# load data from .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

father_id = 905143300
sticker_uid_values = {
    "AQADpwsAAo1TYEly" : 10,
    "AQADVgsAAvl0aEly" : 50,
    "AQAD6w8AApJ2YUly" : -10,
    "AQAD8gsAAuATYUly" : -50
}

database_settings = {
    "host" : os.getenv("db_host"),
    "user" : os.getenv("db_user"),
    "password" : os.getenv("db_password"),
    "database" : os.getenv("db_database")
}

help_text = f"""Привіт я <b>{'Дія.Рейтинг'}</b> бот, я рахую рейтинг учасників в чаті.

Щоб повисити/понизити рейтинг учасника зроби на його повідомлення (reply) і вибери з {hlink('стікерпаку', 'https://t.me/addstickers/DiiaRating')} Дії бал на який ти хочеш оцінити свого співрозмовника.

Доступні команди:
/help — Правила користування ботом
/top — Вивести топ всіх учасників по рейтингу
/rating — Вивести свій рейтинг

Я працюю в будь-яких групах, тому ти можеш добавити мене кудись ще"""