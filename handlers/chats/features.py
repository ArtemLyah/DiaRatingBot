from aiogram import Router, filters, types
from services import RatingService
from services import UserService
from utils.parsing.casualties import ParsingCalualties
from utils.parsing import parse_alert_map, parse_exchange
from datetime import datetime

from .rating import rating_router 
from .rusak import rusak_router 

features_router = Router()
features_router.include_router(rating_router)
features_router.include_router(rusak_router)

rating_service = RatingService()
user_service = UserService()
casualties = ParsingCalualties()

@features_router.message(filters.Command("casualties"))
async def handle_casualties(message: types.Message):
    stats = casualties.get_casualties()
    date = datetime.now().date().isoformat()
    text = f"Статистика втрат ворога на {date}\n"+\
           f"🐷 {stats[12]}\n"+\
           f"🚛 {stats[1]}\n"+\
           f"🚜 {stats[0]}\n"+\
           f"🚗 {stats[10]}\n"+\
           f"💣 {stats[2]}\n"+\
           f"🔥 {stats[3]}\n"+\
           f"✈️ {stats[5]}\n"+\
           f"🚁 {stats[6]}\n"+\
           f"🚀 {stats[7]}\n"+\
           f"🚢 {stats[9]}"
    await message.answer(text)

@features_router.message(filters.Command("alert"))
async def alert_map(message: types.Message):
	await message.answer_document(document=parse_alert_map())

@features_router.message(filters.Command("dollar_rate"))
async def exchange_rate(message: types.Message):
    date = datetime.now().date().isoformat()
    rate = parse_exchange()
    await message.reply(f"💵 Курс доллара до гривні на {date} становить: {rate} грн")