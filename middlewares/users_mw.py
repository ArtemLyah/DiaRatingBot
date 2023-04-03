from aiogram import types, BaseMiddleware
from services import UserService, CountingsService, GroupService
from config import ADMINS
from typing import *

user_service = UserService()
group_service = GroupService()
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
                group = event.message.chat
            case types.Message:
                user = event.from_user
                group = event.chat
            case _:
                return

        user = user_service.addUser(user.id, user.full_name, user.username)
        group_service.addGroup(group.id, group.full_name)
        userGroup = user_service.addUserGroup(group.id, user.id)
        if userGroup.is_ban and not user.id in ADMINS:
            return
        data["db_user"] = user
        data["db_userGroup"] = userGroup
        data["db_counting"] = counting_service.addCountings(user.id)
        await handler(event, data)