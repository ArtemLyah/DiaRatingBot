from aiogram import types, BaseMiddleware
from services import UserService, CountingsService, GroupService
from config import ADMINS
from typing import *

class UsersMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.user_service = UserService()
        self.group_service = GroupService()
        self.counting_service = CountingsService()

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

        user = self.user_service.addUser(user.id, user.full_name, user.username)
        self.group_service.addGroup(group.id, group.full_name)
        userGroup = self.user_service.addUserGroup(group.id, user.id)

        if userGroup.is_ban and not user.id in ADMINS:
            return
        
        data["db_user"] = user
        data["db_userGroup"] = userGroup
        data["db_counting"] = self.counting_service.addCountings(user.id)
        await handler(event, data)