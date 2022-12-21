from aiogram import types, filters
from aiogram.utils.exceptions import RetryAfter
from dispatcher import dp
from filters import IsGroup
from logs import logger
from utils.message_texts import progres_check_content, result_check_content
import random
import asyncio

@dp.message_handler(filters.Command(["check_content"]), IsGroup())
async def check_cringe(message:types.Message):
    if not message.reply_to_message:
        await message.answer("Зробіть reply на повідомлення, щоб перевірити стан контенту")
        return
    try:
        max_progres = 35
        progres = 0
        text = "⚠️ Перевірка контенту ⚠️\n⌛️ Рівень перевірки ⏳ 0%\n🔴🔴🔴\n👮‍♂️ Початок аналізу"
        progres_message = await message.answer(text)
        while progres < max_progres:
            progres += random.randint(5, 8)
            if progres >= max_progres: progres = max_progres

            text = f"⚠️ Перевірка контенту ⚠️\n⌛️ Рівень перевірки ⏳ {round(progres/max_progres*100)}%\n"
            if progres/max_progres < 0.33:
                subtext = random.choice(progres_check_content[0])
                text += "🟢🔴🔴\n"+subtext
            elif progres/max_progres < 0.66:
                subtext = random.choice(progres_check_content[1])
                text += "🟢🟢🔴\n"+subtext
            elif progres/max_progres < 1:
                subtext = random.choice(progres_check_content[2])
                text += "🟢🟢🟢\n"+subtext

            await progres_message.edit_text(text)
            await asyncio.sleep(random.randint(5, 10)/10)
        else:
            level = random.randrange(0, len(result_check_content))
            result_text = result_check_content[level]
            await message.reply_to_message.reply(result_text)
    except RetryAfter:
        await asyncio.sleep(60)
        await message.reply_to_message.reply("4️⃣0️⃣4️⃣\nВаш текст настільки складно розпізнати, що сервера детектору упали!\nЗробіть заклик пізніше")