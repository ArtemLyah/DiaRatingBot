from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from databases import *
from config import father_id
from logs import logger

def add_new_user(message:types.Message, reply_user:types.User):
    if not users.get_info(reply_user.id):
            users.add(
                user_id=reply_user.id,
                username=reply_user.username,
                fullname=reply_user.full_name,
            )
    if not users_status.get_status(message.chat.id, reply_user.id):
        users_status.add_status(message.chat.id, reply_user.id)

class GetDBUserMiddleware(BaseMiddleware):
    # name function on_process_ -> use needed handler (message_handler, callback_query_handler, ...)
    async def on_process_message(self, message:types.Message, data:dict):
        if not message.reply_to_message:
            return
        
        reply_user = message.reply_to_message.from_user
        sender_rating = users_status.rating.get_rating(message.chat.id, message.from_user.id)
        
        add_new_user(message, reply_user)

        if message.content_type == types.ContentType.STICKER:
            rate = stickers.get_info(message.sticker.thumb.file_unique_id)
            if not rate:
                return
            logger.info(f"Sticker of rating was sent")
            logger.info(f"User sender <id={message.from_user.id}, name={message.from_user.full_name}>")
            logger.info(f"Reply user <id={reply_user.id}, name={reply_user.full_name}>")

            # check wether user is cheater
            data["is_cheater"] = message.from_user.id == reply_user.id and reply_user.id != father_id
            if data["is_cheater"] and rate > 0:
                logger.info(f"User <id={message.from_user.id}, name={message.from_user.full_name}> is cheater")
                rate = -50
            elif users_status.isban.get_ban(message.chat.id, reply_user.id):
                data["isban"] = rate > 0
                if rate > 0: return

            # set new rating of reply user
            new_rating = users_status.rating.set_rating(
                group_id=message.chat.id,
                user_id=reply_user.id,  
                rating=rate
            )
            data["new_rating"] = new_rating
            logger.info(f"New rating of reply user "
                        f"<id={reply_user.id}, name={reply_user.full_name}, rating={new_rating}>")

        elif sender_rating and \
            (message.from_user.id == father_id or sender_rating > 2000) and \
            message.text == "/dia_ban":

            logger.info(f"Dia ban for user "
                        f"<id={message.from_user.id}, name={message.from_user.full_name}>")
            if users_status.isban.get_ban(message.chat.id, reply_user.id): 
                return
            users_status.isban.set_ban(message.chat.id, reply_user.id, True)
            data["isban"] = True
            new_rating = users_status.rating.set_rating(message.chat.id, reply_user.id, -1000000)
            data["new_rating"] = new_rating
            logger.info(f"New rating of reply user "
                f"<id={reply_user.id}, name={reply_user.full_name}, rating={new_rating}>")

        elif sender_rating and \
            (message.from_user.id == father_id or sender_rating > 2000) and \
            message.text == "/dia_unban":

            logger.info(f"Dia unban for user "
                        f"<id={message.from_user.id}, name={message.from_user.full_name}>")
            if not users_status.isban.get_ban(message.chat.id, reply_user.id): 
                return
            users_status.isban.set_ban(message.chat.id, reply_user.id, False)
            data["isunban"] = True
            new_rating = users_status.rating.set_rating(message.chat.id, reply_user.id, 1000000)
            data["new_rating"] = new_rating
            logger.info(f"Dia unban for user "
                    f"<id={message.from_user.id}, name={message.from_user.full_name}, rating={new_rating}>")
    
    async def on_process_callback_query(self, query:types.CallbackQuery, data:dict):
        pass