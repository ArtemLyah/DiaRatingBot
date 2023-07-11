from aiogram import types, BaseMiddleware
from databases import Stickers
from loader import db_session
from typing import *

class StickerRatingMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        sticker = event.sticker
        if sticker:
            sticker:Stickers = db_session.query(Stickers)\
                .filter(Stickers.file_id == sticker.file_unique_id).first()
            data["rating"] = sticker.rating if sticker else None
        await handler(event, data)