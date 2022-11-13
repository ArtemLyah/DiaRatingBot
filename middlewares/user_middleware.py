from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from dispatcher import db
from config import father_id

class GetDBUserMiddleware(BaseMiddleware):
    # name function on_process_ -> use needed handler (message_handler, callback_query_handler, ...)
    async def on_process_message(self, message:types.Message, data:dict):
        if message.reply_to_message and message.content_type == types.ContentType.STICKER:
            rate = db.sticker_info.get_rate(message.sticker.thumb.file_unique_id)
            if rate:
                rate = rate[0]
                data["is_cheater"] = message.from_user.id == message.reply_to_message.from_user.id
                # if not data["is_cheater"] and (rate >= 1000 or rate <= -1000):
                #     data["is_cheater"] = message.from_user.id != father_id
                #     data["big_rate"] = rate
                if data["is_cheater"]:
                    data["is_cheater"] = rate > 0
                
                if data["is_cheater"]:
                    user_id = message.from_user.id
                    username = message.from_user.username
                    fullname = message.from_user.full_name
                    rate = -50
                else:
                    reply_message = message.reply_to_message
                    user_id = reply_message.from_user.id
                    username = reply_message.from_user.username
                    fullname = reply_message.from_user.full_name
                if not db.user.get_info(user_id):
                    db.user.add(
                        group_id=message.chat.id,
                        user_id=user_id,
                        username=username,
                        fullname=fullname,
                    )
                if not db.get_rating(message.chat.id, user_id):
                    db.add_rating(message.chat.id, user_id)
                data["new_rating"] = db.set_rating(
                    group_id=message.chat.id,
                    user_id=user_id,  
                    rating=rate
                )
    async def on_process_callback_query(self, query:types.CallbackQuery, data:dict):
        pass