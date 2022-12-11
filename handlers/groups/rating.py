from aiogram import filters, types
from dispatcher import dp
from databases import *
from utils.message_texts import status_text, format_toplist
from filters import IsGroup, IsReplyDiaStickers, IsFather
from logs import logger

@dp.message_handler(filters.Command(["top"]), IsGroup())
async def get_top(message:types.Message):
    toplist = users_status.get_top_by_rating(message.chat.id)
    await message.answer(format_toplist(toplist))
    logger.info(f"Get toplist of group <id={message.chat.id}, name={message.chat.full_name}>")

@dp.message_handler(filters.Command(["rating"]), IsGroup())
async def my_rating(message:types.Message):

    if message.reply_to_message:
        reply_user = message.reply_to_message.from_user
        reply_user_rating = users_status.rating.get_rating(message.chat.id, reply_user.id)
        if reply_user_rating:
            await message.reply(f"Рейтинг у {reply_user.full_name} становить: {reply_user_rating} балів\n{status_text(reply_user_rating)}")
        else:
            await message.reply(f"{reply_user.full_name} ще не отримав/ла бали")
    else:
        user_rating = users_status.rating.get_rating(message.chat.id, message.from_user.id)
        if user_rating:
            await message.reply(f"Твій рейтинг становить: {user_rating} балів\n{status_text(user_rating)}")
        else:
            await message.reply(f"Ти ще не отримав/ла бали")
        logger.info(f"Get rating of user <id={message.from_user.id}, name={message.from_user.full_name}>")

@dp.message_handler(IsGroup(), IsFather(), filters.Command(["dia_ban"]))
async def ban_rating(message:types.Message, new_rating=0, isban=False):
    if not message.reply_to_message:
        return
    if isban:
        await message.answer(f"{message.reply_to_message.from_user.full_name} було тотально знищено й забанено!!! Слава Україні!")
        await message.answer(f"Рейтинг у {message.reply_to_message.from_user.full_name} тепер становить {new_rating}!")
    else:
        await message.answer(f"{message.reply_to_message.from_user.full_name} вже забанено!")
@dp.message_handler(IsGroup(), IsFather(), filters.Command(["dia_unban"]))
async def ban_rating(message:types.Message, new_rating=0, isunban=False):
    if not message.reply_to_message:
        return
    if isunban:
        await message.answer(f"{message.reply_to_message.from_user.full_name} розбанено!!!\nСподіваємось ви нас не розчаруєте! Слава Україні!")
        await message.answer(f"Рейтинг у {message.reply_to_message.from_user.full_name} тепер становить {new_rating}!")
    else:
        await message.answer(f"{message.reply_to_message.from_user.full_name} не було забанено!")

@dp.message_handler(IsReplyDiaStickers(), IsGroup(), content_types=types.ContentTypes.STICKER)
async def increase_rating(message:types.Message, new_rating=0, is_cheater=False, isban=False):
    reply_user = message.reply_to_message.from_user
    if is_cheater:
        await message.reply_sticker("CAACAgIAAx0CbprKMgACA0pjVXxR0_nkabtuQxJax8PXxLtIRwAC8gsAAuATYUnr_8GD-UUo9SoE")
        await message.reply(f"👎 {message.from_user.full_name} - чітер, який намагався повисити свій рейтинг 👎")
        await message.answer(f"Рейтинг у чітера тепер становить {new_rating} балів\n"+status_text(new_rating))
    elif isban and not new_rating:
        await message.answer(f"{reply_user.full_name} забанений/a й не зможе отримувати позитивні бали.")
    else:
        await message.answer(f"{message.sticker.emoji} Рейтинг у {reply_user.full_name} тепер становить {new_rating} балів {message.sticker.emoji}\n"+status_text(new_rating))

@dp.message_handler(IsGroup(), content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def user_left(message:types.Message):
    users_status.remove_status(message.left_chat_member.id, message.chat.id)
    await message.answer(f"Дія.Рейтинг у {message.left_chat_member.full_name} обнулився!")