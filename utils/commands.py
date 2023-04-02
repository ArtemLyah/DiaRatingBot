from aiogram import types

BOT_COMMANDS = {
    "all_chat" : [
        types.BotCommand(command="help", description="Список команд"),
        types.BotCommand(command="alert", description="Карта тривог"),
        types.BotCommand(command="casualties", description="Статистика втрат"),
        types.BotCommand(command="my_rating", description="Мій дія.рейтинг"),
        types.BotCommand(command="mine", description="Майнинг дія.балів"),
        types.BotCommand(command="top_all_10", description="Топ 10 користувачів дія.ботом"),
        types.BotCommand(command="donbass", description="Знайти свого русака"),
        types.BotCommand(command="rusak", description="Показати мого русака"),
        types.BotCommand(command="kill_rusak", description="Вбити русака"),
        types.BotCommand(command="compare_rusak", description="Порівняти русаків"),
        types.BotCommand(command="dollar_rate", description="Курс доллара до гривні"),
    ],
    "private_chat" : [
        
    ],
    "group" : [
        types.BotCommand(command="check_content", description="Перевірити контент на рівень крінжі"),
        types.BotCommand(command="present", description="Подарувати дія.бали /present @тег людини й кількість балів"),
        types.BotCommand(command="random_day", description="Рандомна подія з рандомним учасником"),
        types.BotCommand(command="top", description="Топ учасників групи"),
    ],
    "father" : [
        types.BotCommand(command="dia_ban", description="Забанити учасника"),
        types.BotCommand(command="dia_unban", description="Розбанити учасника"),
        types.BotCommand(command="add_sticker", description="Добавить стикер"),
        types.BotCommand(command="delete_sticker", description="Удалить стикер"),
        types.BotCommand(command="cancel", description="Сбросить StateMachine"),
    ]
}