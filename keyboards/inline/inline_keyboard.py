from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from .callback_datas import RusakData

def rusak_keyboard(user_id, message_id):
    kb = [
        [
            InlineKeyboardButton(
                text="Піймати русака", 
                callback_data=RusakData(user_id=str(user_id), message_id=str(message_id)).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)