from aiogram.enums.chat_type import ChatType
from datetime import date, datetime, timedelta

def next_update_day() -> date:
    return datetime.now().date() + timedelta(days=1)
  
def chat_is_group(chat_type):
    return chat_type in (ChatType.GROUP, ChatType.SUPERGROUP)