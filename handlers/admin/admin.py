from aiogram import Router, filters, types
from aiogram.fsm.context import FSMContext
from filters import IsAdminFilter
from services import UserService, RatingService

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
    reply_userGroup = user_service.getUserGroup(group.id, reply_user.id)

    if reply_userGroup.is_ban:
        await message.answer(f"{reply_user.first_name} has already been banned")
        return

    user_service.setBan(group.id, reply_user.id, True)
    new_rating = rating_service.addRating(reply_userGroup, -10**6)

    await message.answer(f"{reply_user.first_name} has been banned")
    await message.answer(f"New rating in {reply_user.first_name} is {new_rating}")

@admin_router.message(filters.Command("dia_unban"))
async def dia_unban(message: types.Message):
    if not message.reply_to_message:
        return
    reply_user = message.reply_to_message.from_user
    group = message.chat
    reply_userGroup = user_service.getUserGroup(group.id, reply_user.id)

    if not reply_userGroup.is_ban:
        await message.answer(f"{reply_user.first_name} hasn't been banned")
        return

    user_service.setBan(group.id, reply_user.id, False)
    new_rating = rating_service.addRating(reply_userGroup, 10**6)

    await message.answer(f"{reply_user.first_name} has been unbanned")
    await message.answer(f"New rating in {reply_user.first_name} is {new_rating}")

@admin_router.message(filters.Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("StateMachine was successfuly cleared")