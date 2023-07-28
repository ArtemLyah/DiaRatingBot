from aiogram.utils.markdown import hbold, hlink
from databases import Rusak, Users
import aiofiles
import json
import random
from typing import Tuple


help = f"""Привіт я {hbold('Дія.Рейтинг бот')} 🇺🇦, я рахую рейтинг учасників в чаті .

Щоб повисити/понизити рейтинг учасника зроби на його повідомлення (reply) і вибери з {hlink('стікерпаку', 'https://t.me/addstickers/diamarks')} Дії бал на який ти хочеш оцінити свого співрозмовника.

Доступні команди 🗒
/help — Правила користування ботом
/alert — Карта тривог
/casualties — Статистика втрат ворога
/random_day — Рандомна подія дня з рандомним користувачем дія.бота 

Команди для дія.рейнигу 📊
/my_rating - мій дія.рейтинг
/mine - майнінг дія.балів
/top_all_10 - загальний топ всіх користувачі дія.ботом
/top - топ користувачі дія.ботом у групі
/present - подарувати дія.бали людині. Зроби (reply) на повідомлення й напиши /present та кількість балів які хочеш подарувати.

Русаки 🐷
/donbass - впіймати русака
/rusak - мій русак
/kill_rusak - вбити русака
/compare_rusak - порівняти русаків

Цікафі фічі 💅
/check_content - перевірити контент на рівень крінжі
/dollar_rate - курс доллара до гривні
Напишіть @diaratingbot щоб дізнатися більше цікавинок

Я працюю в будь-яких групах, тому ти можеш добавити мене кудись ще 😉"""

cringe_text = [
    "🆘 Ваш контент сплошний крінж. 🆘\nСБУ слідкуватиме за Вами.",
    "⚠️ Ваш контент містить забагато крінжі. ⚠️\nСлідкуйте за базаром.",
    "☣️ Увага токсична небезпека. ☣️\nНегайно відправляйтесь в ізолятор",
    "🌊 Забагато флуду, залиште чат на 1 годину 🌊",
    "Ваш контент в нормі, але бази не наблюдається.",
    "✅ Ваш контент є вкрай грунтовним. ✅",
    "✅ Оце ви файно базанули. Ми навіть спочатку не втямили! ✅",
    "🇺🇦 Ваш контент дуже патріотичний! Слава Україні 🇺🇦"
]

ideologies = [
    "Анархізм",
    "Великодержавний шовінізм",
    "Імперіалізм",
    "Класичний лібералізм",
    "Комунізм",
    "Консерватизм",
    "Ліберальна демократія",
    "Монархізм",
    "Нацизм",
    "Націонал-анархізм",
    "Націонал-більшовизм",
    "Націонал-комунізм",
    "Націоналізм",
    "Неофашизм",
    "Республіканізм",
    "Рашизм",
    "Соціал-демократія",
    "Соціалізм",
    "Сталінізм",
    "Тоталітаризм",
    "Український націоналізм",
    "Фашизм",
    "Християнська демократія",
    "Центризм",
    "Неокомунізм",
]

spots_exercises = [
    "Присідання",
    "Віджимання",
    "Прес",
]

async def topics():
    async with aiofiles.open("data/topics.txt", "r", encoding="utf-8") as file:
        return random.choice(await file.readlines())

async def past_lifes():
    async with aiofiles.open("data/past_life.txt", "r", encoding="utf-8") as file:
        return random.choice(await file.readlines())

async def inline_answers(query: str):
    percentrage = random.randint(0, 100)
    heart = ("💔", "❤️‍🩹", "💜", "💖", "❤️‍🔥")[percentrage//25]
    past_live = await past_lifes()
    ideology = random.choice(ideologies)
    exercise = random.choice(spots_exercises)
    count_of_exercises = random.randint(5, 50)
    topic = await topics()
    return {
        "love" : f"Ви й {query} підходите друг другу на {heart} {percentrage}% {heart}",
        "past_live" : f"В минулому житті ти був {past_live}",
        "ideology" : f"Твоя політична ідеологія: {ideology}",
        "exercises" : f"{exercise} {count_of_exercises} разів!",
        "topic" : f"Щось тихо тут. Давайте поговоримо на тему:\n{topic}"
    }

def rusak_info(user_full_name, name, intelligent, strength, rashism, health):
    emojies = list("🚽🗿🚜☃️🐒🐷🪖🤡💩👽")
    emoji = random.choice(emojies)
    return f"{emoji} Русак у {user_full_name}: \n\n" +\
        f"📝 Ім'я: {name}\n" +\
        f"🧠 Інтелект: {intelligent}\n" +\
        f"💪 Сила: {strength}\n" +\
        f"👽 Рівень рашизму: {rashism}%\n" +\
        f"❤️ Здоров'я: {health}%"

def format_top_10(top):
    result = "Топ 10 найактивніших користувачів Дія.Рейтингом:\n"
    medals = "🏆🎖🏅🥇🥈🥉"
    for i, info in enumerate(top):
        name, rating = info
        if i < len(medals): 
            result += f"{medals[i]} {i+1}. {hbold(name)} - {rating} дія.балів\n"
        else:
            result += f"{i+1}. {hbold(name)} {rating} дія.балів\n"
    return result

def format_top(top):
    result = "Топ користувачів Дія.Рейтингом у групі:\n"
    for i, info in enumerate(top, 1):
        name, rating = info
        if i % 10 == 0: result += "\n"
        result += f"{i}. {hbold(name)} {rating} дія.балів\n"
    return result

def format_comparing_rusak(rusak1: Rusak, rusak2: Rusak):
    return f"{rusak1.name} - {rusak2.name}\n" +\
            f"🧠 Інтелект: {rusak1.intellect} - {rusak2.intellect}\n" +\
            f"💪 Сила: {rusak1.strength} - {rusak2.strength}\n" +\
            f"👽 Рашизм: {rusak1.rashism}% - {rusak2.rashism}%\n" +\
            f"❤️ Здоров'я: {rusak1.health}% - {rusak2.health}%\n"

class FormatStatus():
    filepath = "data/status.json"
    def __init__(self):
        file = open(self.filepath, "r", encoding="utf-8") 
        self.status = json.load(file)
    def __call__(self, text, rating):
        ratings = list(self.status.keys())
        if rating >= int(ratings[-1]):
            return text+"\n"+random.choice(self.status[ratings[-1]])
        elif rating <= int(ratings[0]):
            return text+"\n"+random.choice(self.status[ratings[0]])
        for i, rate in enumerate(ratings):
            rate = int(rate)
            if rating == rate:
                status_id = str(rate)
                break
            elif rate < 0:
                if rating < rate:
                    status_id = str(rate)
                    break
            elif rate > 0:
                if rating < rate:
                    status_id = ratings[i-1] 
                    break
        return text+"\n"+random.choice(self.status[status_id])

format_status = FormatStatus()

class FormatRandomDay():
    filepath = "data/random_day.txt"
    def __init__(self):
        file = open(self.filepath, "r", encoding="utf-8") 
        self.textlist = file.readlines()
        for i in range(len(self.textlist)):
            self.textlist[i] = self.textlist[i].replace('\\n', '\n')
            self.textlist[i] = self.textlist[i].replace('\\t', '\t')

    def format_text(self, users: list[Users]) -> Tuple[str, int, list[Users]]:
        text_id = random.randrange(0, len(self.textlist))
        text = self.textlist[text_id]
        n_users = text.count('@{}')
        users = random.choices(users, k=n_users)
        usernames = [user.username for user in users]
        return text.format(*usernames), text_id, users
    
    def format_text_by_text_id(self, users: list[Users], text_id) -> str:
        usernames = [user.username for user in users]
        text: str = self.textlist[text_id]
        n_users = text.count('@{}')
        while len(usernames) < n_users:
            usernames.append(usernames[-1])
        return text.format(*usernames)

format_random_day = FormatRandomDay()