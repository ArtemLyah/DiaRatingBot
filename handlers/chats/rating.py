from aiogram import Router, filters, types
from aiogram.enums import ChatType
from services import RatingService, UserService, CountingsService
from databases.models import Users, UserGroup, Countings
from datetime import datetime
from data import text
import random

rating_router = Router()
user_service = UserService()
rating_service = RatingService()
counting_service = CountingsService()

@rating_router.message(filters.Command("my_rating"))
async def my_rating(message: types.Message, db_userGroup: UserGroup):
    user = message.from_user
    group = message.chat
    global_rating = rating_service.calculateGlobalRating(user.id)
    answer = f"Ваш глобальний рейтинг становить <b>{global_rating}</b> дія.балів\n"
    if message.chat.type == ChatType.GROUP or message.chat.type == ChatType.SUPERGROUP:
        local_rating = db_userGroup.local_rating
        answer += f"Ваш локальний рейтинг в {group.full_name} становить <b>{local_rating}</b> дія.балів"
        answer = text.format_status(answer, local_rating)
    else:
        answer = text.format_status(answer, global_rating)
    await message.reply(answer)    
    

@rating_router.message(filters.Command("top_all_10"))
async def top_all_10(message: types.Message):
    top_10 = rating_service.get_top_10()
    await message.answer(text.format_top_10(top_10))

@rating_router.message(filters.Command("mine"))
async def mine_rating(
    message: types.Message, 
    db_user: Users, 
    db_userGroup: UserGroup, 
    db_counting: Countings
):
    count_mining = db_counting.count_mining

    if datetime.now().date() >= db_counting.update_limit_date:
        counting_service.resetCountings(db_user.id)
        count_mining = 0
    elif count_mining >= 15:
        await message.reply("Ваш щоденний ліміт на майнінг вичерпався")
        return

    counting_service.updateCounting(
        Countings.count_mining, 
        db_user.id, 
        count_mining+1
    )

    i = random.randint(1, 100)
    rating = 0
    if i == 1:
        rating = 100
    elif i < 3:
        rating = 50
    elif i < 5:
        rating = 10
    elif i < 9:
        rating = 5
    elif i < 15:
        rating = 1
    else:
        return
    
    new_rating = rating_service.addRating(db_userGroup, rating)
    await message.reply(text.format_status(f"Ви намайнили {rating} дія.балів", new_rating))