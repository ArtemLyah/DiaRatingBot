from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from dispatcher import db

class GetDBUserMiddleware(BaseMiddleware):
    # name function on_process_ -> use needed handler (message_handler, callback_query_handler, ...)
    async def on_process_message(self, message:types.Message, data:dict):
        if message.reply_to_message and message.content_type == types.ContentType.STICKER:
            rate = db.status_info.get_rate(message.sticker.thumb.file_unique_id)
            if rate:
                reply_message = message.reply_to_message
                user = db.user.get_info(reply_message.from_user.id)
                if not user:
                    db.user.add(
                        group_id=message.chat.id,
                        id=reply_message.from_user.id,
                        username=reply_message.from_user.username,
                        fullname=reply_message.from_user.full_name,
                )
                if not db.get_rating(message.chat.id, reply_message.from_user.id):
                    db.add_rating(message.chat.id, reply_message.from_user.id)

                data["is_cheater"] = message.from_user.id == reply_message.from_user.id and rate > 0
                if not data["is_cheater"]:
                    data["new_rating"] = db.set_rating(
                        user_id=reply_message.from_user.id,
                        group_id=message.chat.id,
                        rating=rate
                    )
                else:
                    data["new_rating"] = db.set_rating(
                        user_id=reply_message.from_user.id,
                        group_id=message.chat.id,
                        rating=-50
                    )
                
    async def on_process_callback_query(self, query:types.CallbackQuery, data:dict):
        pass