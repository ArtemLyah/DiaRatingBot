from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Правила користування Дія.рейтинг"),
            types.BotCommand("top", "Топ учасників по рейтингу"),
            types.BotCommand("rating", "Твій теперешій рейтинг"),
        ]
    )