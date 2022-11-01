from aiogram import filters, types
from dispatcher import dp, db
from config import help_text
from utils.status_text import status_text
from filters import IsGroup, IsReplyDiaStickers, IsFather

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
    toplist = "\n".join([f"{i}. <b>{value[0]}</b>: {value[1]} дія.балів" for i, value in enumerate(toplist, 1)])
    await message.answer("Топ учасників по Дія.Рейтингу:\n"+toplist+"\nВсі інші учасники ще не отримали бали")

@dp.message_handler(filters.Command(["rating"]), IsGroup())
async def my_rating(message:types.Message):
    user_info = db.get_rating(message.chat.id, message.from_user.id)
    if user_info:
        await message.answer(f"Твій рейтинг становить: {user_info[0]} балів\n"+status_text(user_info[0]))
    else:
        await message.answer(f"Ти ще не отримав/ла бали, тому твій рейтинг становить 0 балів")

@dp.message_handler(IsGroup(), IsFather(), filters.Command(["ban_rating"]))
async def ban_rating(message:types.Message):
    user_info = db.get_rating(message.chat.id, message.from_user.id)
    if not user_info:
        db.user.add(message.chat.id, message.from_user.id, message.from_user.username, message.from_user.full_name)
    db.set_rating(message.chat.id, message.from_user.id, -1000000)
    await message.answer(f"{message.from_user.full_name} було забанено!!! Слава Україні!")

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
