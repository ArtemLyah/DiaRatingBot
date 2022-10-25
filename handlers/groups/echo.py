from aiogram import filters, types
from dispatcher import dp, db
from config import help_text, status_text
from filters import IsGroup, IsReplyDiaStickers

# handle private messages
@dp.message_handler(filters.CommandStart(), IsGroup())
async def start(message:types.Message):
    await message.answer(help_text)

@dp.message_handler(filters.Command(["help"]), IsGroup())
async def help(message:types.Message):
    await message.answer(help_text)

@dp.message_handler(filters.Command(["top"]), IsGroup())
async def get_top(message:types.Message):
    toplist = db.get_top_by_rating(message.chat.id)
    toplist = "\n".join([f"{i}. {value[0]} {value[1]} балів" for i, value in enumerate(toplist, 1)])
    await message.answer("Топ учасників по Дія.Рейтингу:\n"+toplist+"\nВсі інші учасники ще не отримали бали")

@dp.message_handler(filters.Command(["rating"]), IsGroup())
async def my_rating(message:types.Message):
    user_info = db.get_rating(message.chat.id, message.from_user.id)
    if user_info:
        await message.answer(f"Твій рейтинг становить: {user_info[0]} балів\n"+status_text(user_info[0]))
    else:
        await message.answer(f"Ти ще не отримав/ла бали, тому твій рейтинг становить 0 балів")

@dp.message_handler(IsReplyDiaStickers(), IsGroup(), content_types=types.ContentTypes.STICKER)
async def increase_rating(message:types.Message, new_rating, is_cheater):
    print(new_rating)
    if is_cheater:
        await message.reply_sticker("CAACAgIAAx0CbprKMgACA0pjVXxR0_nkabtuQxJax8PXxLtIRwAC8gsAAuATYUnr_8GD-UUo9SoE")
        await message.reply(f"👎 {message.from_user.full_name} - чітер, який намагався повисити свій рейтинг 👎")
        await message.answer(f"Рейтинг у чітера тепер становить {new_rating} балів\n"+status_text(new_rating))
    else:
        fullname = message.reply_to_message.from_user.full_name
        await message.answer(f"{message.sticker.emoji} Рейтинг у {fullname} тепер становить {new_rating} балів {message.sticker.emoji}\n"+status_text(new_rating))
