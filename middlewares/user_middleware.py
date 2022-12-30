from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from databases import *
from config import FATHER_ID
from logs import logger

def add_new_user(group_id, reply_user:types.User):
    if not users.get_info(reply_user.id):
        users.add(
            user_id=reply_user.id,
            username=reply_user.username,
            fullname=reply_user.full_name,
        )
    if not user_status.get_status(group_id, reply_user.id):
        user_status.add_status(group_id, reply_user.id)

class GetDBUserMiddleware(BaseMiddleware):
    # name function on_process_ -> use needed handler (message_handler, callback_query_handler, ...)
    async def on_process_message(self, message:types.Message, data:dict):
        if not message.reply_to_message:
            return
        
        group_id = message.chat.id
        from_user = message.from_user
        reply_user = message.reply_to_message.from_user
        from_user_rating = user_status.rating.get_rating(group_id, from_user.id)

        add_new_user(group_id, reply_user)

        if message.content_type == types.ContentType.STICKER:
            rate = stickers.get_info(message.sticker.thumb.file_unique_id)
            if not rate:
                return
            logger.info(f"Sticker of rating was sent")
            logger.info(f"User sender <id={from_user.id}, name={from_user.full_name}>")
            logger.info(f"Reply user <id={reply_user.id}, name={reply_user.full_name}>")

            # check wether user is cheater
            data["is_cheater"] = (from_user.id == reply_user.id and reply_user.id != FATHER_ID) and rate > 0
            if data["is_cheater"]:
                logger.info(f"User <id={from_user.id}, name={from_user.full_name}> is cheater")
                rate = -50
            # if isban and rate > 0 then don't increase rating
            elif user_status.isban.get_ban(group_id, reply_user.id):
                data["isban"] = rate > 0
                if rate > 0: return

            # set new rating of reply user
            new_rating = user_status.rating.set_rating(
                group_id=group_id,
                user_id=reply_user.id,  
                increase_rating=rate
            )
            data["new_rating"] = new_rating
            logger.info(f"New rating of reply user "
                        f"<id={reply_user.id}, name={reply_user.full_name}, rating={new_rating}>")

        elif from_user_rating and \
            (from_user.id == FATHER_ID or from_user_rating > 2000) and \
            message.text == "/dia_ban":

            logger.info(f"Dia ban for user "
                        f"<id={from_user.id}, name={from_user.full_name}>")
            if user_status.isban.get_ban(group_id, reply_user.id): 
                return

            user_status.isban.set_ban(group_id, reply_user.id, True)
            data["isban"] = True
            new_rating = user_status.rating.set_rating(
                group_id=group_id,
                user_id=reply_user.id,  
                increase_rating=-1000000
            )
            data["new_rating"] = new_rating
            logger.info(f"New rating of reply user "
                f"<id={reply_user.id}, name={reply_user.full_name}, rating={new_rating}>")

        elif from_user_rating and \
            (from_user.id == FATHER_ID or from_user_rating > 2000) and \
            message.text == "/dia_unban":

            logger.info(f"Dia unban for user "
                        f"<id={from_user.id}, name={from_user.full_name}>")
            if not user_status.isban.get_ban(group_id, reply_user.id): 
                return

            user_status.isban.set_ban(group_id, reply_user.id, False)
            data["isunban"] = True
            new_rating = user_status.rating.set_rating(
                group_id=group_id,
                user_id=reply_user.id,  
                increase_rating=-1000000
            )
            data["new_rating"] = new_rating
            data["new_rating"] = new_rating
            logger.info(f"Dia unban for user "
                    f"<id={from_user.id}, name={from_user.full_name}, rating={new_rating}>")
    
    async def on_process_callback_query(self, query:types.CallbackQuery, data:dict):
        pass