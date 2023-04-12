from aiogram import types, BaseMiddleware
from utils.logs import logger
from typing import *
from utils.mics import chat_is_group

class LoggingMessageMiddleware(BaseMiddleware):
    async def __call__ (self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        
        chat_id = event.chat.id
        user_id = event.from_user.id
        text = event.text

        if text and chat_is_group(event.chat.type) and not text.startswith("/"):
            return
        logger.debug(f"[Message] gid: {chat_id} | uid: {user_id} | text: {text}")
        return await handler(event, data)

class LoggingCallbackMiddleware(BaseMiddleware):
    async def __call__ (self,
        handler: Callable[[types.CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: types.CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        chat_id = event.message.chat.id
        user_id = event.from_user.id
        callback_data = event.data

        logger.debug(f"[CallbackQuery] gid: {chat_id} | uid: {user_id} callback_data: {callback_data}")
        return await handler(event, data)

class LoggingInlineMiddleware(BaseMiddleware):
    async def __call__ (self,
        handler: Callable[[types.InlineQuery, Dict[str, Any]], Awaitable[Any]],
        event: types.InlineQuery,
        data: Dict[str, Any]
    ) -> Any:        

        query = event.query        
        user_id = event.from_user.id

        logger.debug(f"[InlineQuery] uid: {user_id} | query: \"{query}\"")
        return await handler(event, data)