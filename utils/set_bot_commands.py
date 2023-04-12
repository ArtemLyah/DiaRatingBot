from aiogram import Bot, types
from aiogram.types.bot_command_scope_chat_member import BotCommandScopeChatMember
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
from aiogram.types.bot_command_scope_all_group_chats import BotCommandScopeAllGroupChats
from .commands import BOT_COMMANDS
from config import ADMINS

async def add_admin_commands_to_chat(bot:Bot, chat_id: int):
    for admin_id in ADMINS:
        await bot.set_my_commands(
            commands=BOT_COMMANDS["all_chat"]+BOT_COMMANDS["group"]+BOT_COMMANDS["father"],
            scope=BotCommandScopeChatMember(chat_id=chat_id, user_id=admin_id)
        )

async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        commands=BOT_COMMANDS["all_chat"]+BOT_COMMANDS["private_chat"]+BOT_COMMANDS["father"],
        scope=BotCommandScopeAllPrivateChats()
    )
    await bot.set_my_commands(
        commands=BOT_COMMANDS["all_chat"]+BOT_COMMANDS["group"],
        scope=BotCommandScopeAllGroupChats()
    )
