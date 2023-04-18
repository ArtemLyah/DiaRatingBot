from aiogram import Router, filters, types
from aiogram.fsm.context import FSMContext
from filters import IsAdminFilter
from services import UserService, RatingService
from data.text import format_status
from .sticker_settings import sticker_settings_router

admin_router = Router()
admin_router.include_router(sticker_settings_router)
admin_router.message.filter(IsAdminFilter())

user_service = UserService()
rating_service = RatingService()

@admin_router.message(filters.Command("dia_ban"))
async def dia_ban(message: types.Message):
    if not message.reply_to_message:
        return
    reply_user = message.reply_to_message.from_user
    group = message.chat
    reply_userGroup = user_service.addUserGroup(group.id, reply_user.id)

    if reply_userGroup.is_ban:
        await message.reply(f"{reply_user.first_name} вже забанений/a.")
        return

    user_service.setBan(group.id, reply_user.id, True)
    new_rating = rating_service.addRating(reply_userGroup, -10**6)

    await message.reply(f"{reply_user.first_name} було забанено та знищено")
    await message.answer(format_status(f"Рейтинг у {reply_user.first_name} тепер становить {new_rating}", new_rating))

@admin_router.message(filters.Command("dia_unban"))
async def dia_unban(message: types.Message):
    if not message.reply_to_message:
        return
    reply_user = message.reply_to_message.from_user
    group = message.chat
    reply_userGroup = user_service.getUserGroup(group.id, reply_user.id)

    if not reply_userGroup.is_ban:
        await message.reply(f"{reply_user.first_name} не був/ла забанений/а")
        return

    user_service.setBan(group.id, reply_user.id, False)
    new_rating = rating_service.addRating(reply_userGroup, 10**6)

    await message.reply(f"{reply_user.first_name} успішно розбанено! Сподіваємось ви нас не розчаруєте")
    await message.answer(format_status(f"Новий рейтинг у {reply_user.first_name} становить {new_rating}", new_rating))

@admin_router.message(filters.Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("StateMachine was successfuly cleared")