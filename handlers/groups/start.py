from aiogram import Router, Bot, filters, types
from aiogram.enums.chat_type import ChatType
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter 
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, IS_MEMBER 
from loader import bot
from filters import ChatTypeFilter
from services.group_service import GroupService
from utils.set_bot_commands import add_admin_commands_to_chat
from data import text

from .rating import rating_router
from .features import feature_router

group_router = Router()
group_router.include_router(feature_router)
group_router.include_router(rating_router)
group_router.message.filter(ChatTypeFilter((ChatType.GROUP, ChatType.SUPERGROUP)))

group_service = GroupService()

@group_router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=(IS_NOT_MEMBER >> IS_MEMBER)
    )
)
async def join_group(event: types.ChatMemberUpdated, bot: Bot):
    chat = event.chat
    await add_admin_commands_to_chat(bot, chat.id)
    group_service.addGroup(chat.id, chat.full_name)
    await bot.send_message(chat.id, text.help)

@group_router.message(filters.CommandStart())
async def start(message: types.Message):
    chat = message.chat
    await add_admin_commands_to_chat(bot, chat.id)
    await message.answer(text.help)

@group_router.message(filters.Command("help"))
async def help(message: types.Message):
    await message.answer(text.help)


