from aiogram import filters, types
from dispatcher import dp, db
from utils.message_texts import status_text, format_toplist, help
from filters import IsGroup, IsReplyDiaStickers, IsFather

# handle private messages
@dp.message_handler(filters.CommandStart(), IsGroup())
async def start(message:types.Message):
    await message.answer(help)
    db.group.add(message.chat.id, message.chat.username, message.chat.full_name)

@dp.message_handler(filters.Command(["help"]), IsGroup())
async def help(message:types.Message):
    await message.answer(help)

@dp.message_handler(filters.Command(["top"]), IsGroup())
async def get_top(message:types.Message):
    toplist = db.get_top_by_rating(message.chat.id)
    await message.answer(format_toplist(toplist))

@dp.message_handler(filters.Command(["rating"]), IsGroup())
async def my_rating(message:types.Message):
    user_info = db.get_rating(message.chat.id, message.from_user.id)
    if user_info:
        await message.reply(f"Твій рейтинг становить: {user_info[0]} балів\n"+status_text(user_info[0]))
    else:
        await message.reply(f"Ти ще не отримав/ла бали, тому твій рейтинг становить 0 балів")

@dp.message_handler(IsGroup(), IsFather(), filters.Command(["dia_ban"]))
async def ban_rating(message:types.Message, new_rating=0):
    await message.answer(f"{message.reply_to_message.from_user.full_name} було тотально знищено!!! Слава Україні!")
    await message.answer(f"Рейтинг у {message.reply_to_message.from_user.full_name} тепер становить {new_rating}!")

@dp.message_handler(IsReplyDiaStickers(), IsGroup(), content_types=types.ContentTypes.STICKER)
async def increase_rating(message:types.Message, new_rating, is_cheater):
    if is_cheater:
        await message.reply_sticker("CAACAgIAAx0CbprKMgACA0pjVXxR0_nkabtuQxJax8PXxLtIRwAC8gsAAuATYUnr_8GD-UUo9SoE")
        await message.reply(f"👎 {message.from_user.full_name} - чітер, який намагався повисити свій рейтинг 👎")
        await message.answer(f"Рейтинг у чітера тепер становить {new_rating} балів\n"+status_text(new_rating))
    else:
        fullname = message.reply_to_message.from_user.full_name
        await message.answer(f"{message.sticker.emoji} Рейтинг у {fullname} тепер становить {new_rating} балів {message.sticker.emoji}\n"+status_text(new_rating))

@dp.message_handler(IsGroup(), content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def user_left(message:types.Message):
    db.user.remove_rating(message.left_chat_member.id, message.chat.id)
    await message.answer(f"Дія.Рейтинг у {message.left_chat_member.full_name} обнулився!")