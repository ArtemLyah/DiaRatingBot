from aiogram.filters.callback_data import CallbackData

class RusakData(CallbackData, prefix="rusak"):
    user_id: str
    message_id: str