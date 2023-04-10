from aiogram import Router, F, filters, types
from data import text

inline_router = Router()

@inline_router.inline_query()
async def inline_handler(inline_query: types.InlineQuery):
    answers = await text.inline_answers(inline_query.query)
    results = [
        types.InlineQueryResultArticle(
            id = "1",
            title = "Наскільки ви підходите один одному",
            description="Напишіть ім'я людини з якою бажаєте перевірити свої почуття",
            thumb_url="https://images.wallpaperscraft.ru/image/single/para_siluety_noch_119106_225x300.jpg",
            input_message_content=types.InputTextMessageContent(
                message_text=answers["love"]
            )
        ),
        types.InlineQueryResultArticle(
            id = "2",
            title = "Ким ти був в минулому житті?",
            description="",
            thumb_url="https://misis.ru/files/6803/3_1.jpeg",
            input_message_content=types.InputTextMessageContent(
                message_text=answers["past_live"]
            )
        ),
        types.InlineQueryResultArticle(
            id = "3",
            title = "Твоя ідеологія",
            thumb_url="https://static7.depositphotos.com/1220104/711/i/450/depositphotos_7112291-stock-photo-demokrats-button-isolated-on-white.jpg",
            input_message_content=types.InputTextMessageContent(
                message_text=answers["ideology"]
            )
        ),
        types.InlineQueryResultArticle(
            id = "4",
            title = "Хвилинка фізичних вправ",
            description="Ти ж ніколи не зробиш це, чи не так?",
            thumb_url="https://androshchuk.com/wp-content/uploads/2021/12/original_large.jpg",
            input_message_content=types.InputTextMessageContent(
                message_text=answers["exercises"]
            )
        ),
        types.InlineQueryResultArticle(
            id = "5",
            title = "Тема для розмови",
            description="Допоможе підняти активчик в групі",
            thumb_url="https://st2.depositphotos.com/2604049/5210/i/950/depositphotos_52107473-stock-photo-light-bulb-metaphor-for-good.jpg",
            input_message_content=types.InputTextMessageContent(
                message_text=answers["topic"]
            )
        ),
    ]
    await inline_query.answer(results, cache_time=1, is_personal=True)
