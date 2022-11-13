from aiogram import filters, types
from dispatcher import dp, db
from config import help_text
from utils.status_text import status_text
from filters import IsGroup, IsReplyDiaStickers, IsFather
import math

# handle private messages
@dp.message_handler(filters.CommandStart(), IsGroup())
async def start(message:types.Message):
    await message.answer(help_text)
    db.group.add(message.chat.id, message.chat.username, message.chat.full_name)

@dp.message_handler(filters.Command(["help"]), IsGroup())
async def help(message:types.Message):
    await message.answer(help_text)

@dp.message_handler(filters.Command(["top"]), IsGroup())
async def get_top(message:types.Message):
    toplist = db.get_top_by_rating(message.chat.id)
    await message.answer("Топ учасників по Дія.Рейтингу:")
    for i in range(math.ceil(len(toplist)/10)):
        toplist_text = "" 
        for j in range(i*10, (i+1)*10):
            if j >= len(toplist):
                break
            toplist_text += f"{j}. <b>{toplist[j][0]}</b>: {toplist[j][1]} дія.балів\n"
        await message.answer(toplist_text)

@dp.message_handler(filters.Command(["rating"]), IsGroup())
async def my_rating(message:types.Message):
    user_info = db.get_rating(message.chat.id, message.from_user.id)
    if user_info:
        await message.reply(f"Твій рейтинг становить: {user_info[0]} балів\n"+status_text(user_info[0]))
    else:
        await message.reply(f"Ти ще не отримав/ла бали, тому твій рейтинг становить 0 балів")

@dp.message_handler(IsGroup(), IsFather(), filters.Command(["dia_ban"]))
async def ban_rating(message:types.Message):
    user_info = db.user.get_info(message.from_user.id)
    reply_message = message.reply_to_message
    if not user_info:
        db.user.add(message.chat.id, reply_message.from_user.id, reply_message.from_user.username, reply_message.from_user.full_name)
    new_rating = db.set_rating(message.chat.id, reply_message.from_user.id, -1000000)
    await message.answer(f"{reply_message.from_user.full_name} було тотально знищено!!! Слава Україні!")
    await message.answer(f"Рейтинг у {reply_message.from_user.full_name} тепер становить {new_rating}!")

@dp.message_handler(IsReplyDiaStickers(), IsGroup(), content_types=types.ContentTypes.STICKER)
async def increase_rating(message:types.Message, new_rating, is_cheater, big_rate=0):
    if is_cheater:
        await message.reply_sticker("CAACAgIAAx0CbprKMgACA0pjVXxR0_nkabtuQxJax8PXxLtIRwAC8gsAAuATYUnr_8GD-UUo9SoE")
        # if big_rate != 0:
        #     await message.reply(f"👎 {message.from_user.full_name} - чітер, який намагався використати великі бали 👎")
        #     await message.answer(f"Великі бали використовує тільки розробник боту!!!")
        # else:
        await message.reply(f"👎 {message.from_user.full_name} - чітер, який намагався повисити свій рейтинг 👎")
        await message.answer(f"Рейтинг у чітера тепер становить {new_rating} балів\n"+status_text(new_rating))
    else:
        fullname = message.reply_to_message.from_user.full_name
        await message.answer(f"{message.sticker.emoji} Рейтинг у {fullname} тепер становить {new_rating} балів {message.sticker.emoji}\n"+status_text(new_rating))

@dp.message_handler(IsGroup(), content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def user_left(message:types.Message, left_chat_member:types.User):
    if left_chat_member:
        await message.answer(f"Дія.Рейтинг у {left_chat_member.full_name} обнулився!")