from aiogram import Router, types, filters, F
from aiogram.enums import ChatType
from filters import ChatTypeFilter
from services import UserService, RatingService, UserRandomService
from datetime import datetime
from data import text
import random

feature_router = Router()
feature_router.message.filter(ChatTypeFilter((ChatType.GROUP, ChatType.SUPERGROUP)))
user_service = UserService()
rating_service = RatingService()
user_random_service = UserRandomService()

@feature_router.message(filters.Command("top"))
async def top_group(message: types.Message):
    group = message.chat
    top = rating_service.get_top_group(group.id)
    await message.answer(text.format_top(top))

@feature_router.message(filters.Command("random_day"))
async def get_random(message:types.Message): 
    group = message.chat
    rand_users = user_random_service.getUsersRandom(group.id)
    if len(rand_users) == 0:
        userlist = user_service.getAllUsersInGroup(group.id)
        result, text_id, users = text.format_random_day.format_text(userlist)
        user_random_service.addUsers(group.id, users, text_id)
    elif datetime.now().date() >= rand_users[0][2]:
        userlist = user_service.getAllUsersInGroup(group.id)
        result, text_id, users = text.format_random_day.format_text(userlist)
        user_random_service.updateUsers(group.id, users, text_id)
    else:
        users = [user for user, _, _ in rand_users]
        text_id = rand_users[0][1]
        result = text.format_random_day.format_text_by_text_id(users, text_id)
    await message.answer(result)

@feature_router.message(filters.Command("check_content"))
async def check_content(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Зробіть (reply) на повідомлення щоб перевірити його на рівень крінжі")
        return
    reply_message = message.reply_to_message
    await reply_message.reply(random.choice(text.cringe_text))