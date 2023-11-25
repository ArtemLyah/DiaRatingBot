from aiogram import Bot, types
from aiogram.types.bot_command_scope_chat_member import BotCommandScopeChatMember
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
from aiogram.types.bot_command_scope_all_group_chats import BotCommandScopeAllGroupChats
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat
from .commands import BOT_COMMANDS
from config import ADMINS

async def add_admin_commands_to_chat(bot:Bot, chat_id: int):
    await bot.set_my_commands(
        commands=BOT_COMMANDS["all_chat"]+BOT_COMMANDS["group"]+BOT_COMMANDS["father"],
        scope=BotCommandScopeChatMember(chat_id=chat_id, user_id=ADMINS[0])
    )

async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        commands=BOT_COMMANDS["all_chat"]+BOT_COMMANDS["group"]+BOT_COMMANDS["father"],
        scope=BotCommandScopeChat(chat_id=str(ADMINS[0]))
    )
    await bot.set_my_commands(
        commands=BOT_COMMANDS["all_chat"]+BOT_COMMANDS["private_chat"],
        scope=BotCommandScopeAllPrivateChats()
    )
    await bot.set_my_commands(
        commands=BOT_COMMANDS["all_chat"]+BOT_COMMANDS["group"],
        scope=BotCommandScopeAllGroupChats()
    )
