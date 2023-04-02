from aiogram import types, BaseMiddleware
from services import UserService, CountingsService
from config import ADMINS
from typing import *

user_service = UserService()
counting_service = CountingsService()

class UsersMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Update,
        data: Dict[str, Any]
    ) -> Any:
        match type(event):
            case types.CallbackQuery:
                user = event.message.from_user
                chat = event.message.chat
            case types.Message:
                user = event.from_user
                chat = event.chat
            case _:
                user = event.from_user
                user = event.message.chat

        userGroup = user_service.addUserGroup(chat.id, user.id)
        if userGroup.is_ban and not user.id in ADMINS:
            return
            
        data["db_user"] = user_service.addUser(user.id, user.full_name, user.username)
        data["db_counting"] = counting_service.addCountings(user.id)
        data["db_userGroup"] = userGroup
        await handler(event, data)