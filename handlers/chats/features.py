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

def find_stats(title: str, list: list[str]):
    for elem in list:
        if title in elem:
            return elem
    return ''

@features_router.message(filters.Command("casualties"))
async def handle_casualties(message: types.Message):
    stats = casualties.get_casualties()
    date = datetime.now().date().isoformat()
    text = f"Статистика втрат ворога на {date}\n"+\
           f"🐷 {find_stats('Особовий склад', stats)}\n"+\
           f"🚛 {find_stats('ББМ', stats)}\n"+\
           f"🚜 {find_stats('Танки', stats)}\n"+\
           f"🚗 {find_stats('Автомобілі та автоцистерни', stats)}\n"+\
           f"💣 {find_stats('Артилерійські системи', stats)}\n"+\
           f"🔥 {find_stats('РСЗВ', stats)}\n"+\
           f"✈️ {find_stats('Літаки', stats)}\n"+\
           f"🚁 {find_stats('Гелікоптери', stats)}\n"+\
           f"🚀 {find_stats('Крилаті ракети', stats)}\n"+\
           f"🚢 {find_stats('Кораблі (катери)', stats)}\n"+\
           f"🐟 {find_stats('Підводні човни', stats)}"
    await message.answer(text)

@features_router.message(filters.Command("alert"))
async def alert_map(message: types.Message):
	await message.answer_document(document=parse_alert_map())

@features_router.message(filters.Command("dollar_rate"))
async def exchange_rate(message: types.Message):
    date = datetime.now().date().isoformat()
    rate = parse_exchange()
    await message.reply(f"💵 Курс доллара до гривні на {date} становить: {rate} грн")