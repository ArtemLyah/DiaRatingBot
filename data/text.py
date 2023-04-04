from aiogram.utils.markdown import hbold, hlink
from databases.models import Rusak, Users
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

topics = [
    "Ваша улюблена музика: жанри, виконавці, альбоми, пісні.",
    "Що б ви робили, якщо ви виграли в лотерею?",
    "Якби ви стали безмежно багатим, що б ви робили?",
    "Ваші улюблені фільми та телешоу: жанри, режисери, актори, сценарії.",
    "Що б ви робили, якби у вас було 24 години вільного часу?",
    "Якби ви мали можливість змінити щось у світі, що б ви змінили?",
    "Ваші улюблені книги: жанри, автори, сюжети, герої.",
    "Якби ви могли жити в будь-якій епохі, коли б ви обрали?",
    "Ваші улюблені страви: національна та місцева кухня, рецепти, інгредієнти.",
    "Якби ви мали можливість поговорити з будь-якою історичною постаттю, з ким б ви поговорили та що б запитали?",
    "Ваші улюблені подорожі: країни, міста, пам'ятки, враження.",
    "Якби ви мали можливість побачити будь-яку відому особистість, з ким б ви зустрілися?",
    "Ваші улюблені спортивні змагання: види спорту, команди, спортсмени, результати.",
    "Якби ви мали можливість мати будь-яку професію, що б ви обрали?",
    "Ваші улюблені розваги: ігри, хобі, способи проведення вільного часу.",
    "Якби ви мали можливість жити в будь-якій країні, де б ви жили?",
    "Ваші улюблені місця для відпочинку: готелі, курорти, пляжі, гори.",
    "Ваші улюблені види мистецтва: живопис, скульптура, архітектура, музика, танець, театр.",
    "Якби ви мали можливість змінити щось у своєму житті, що б ви змінили і чому?",
    "Чи можливо створити програму, яка буде робити все за вас, і ви в цей час будете займатися чимось іншим?",
    "Як можна використовувати блокчейн технології в бізнесі?",
    "Якби ви створили свій власний мову програмування, які б у неї були особливості?",
    "Якби комп'ютери могли розуміти людську мову, якби це змінило університетську освіту?",
    "Чи можливо замінити викладачів в університеті на роботів-викладачів?",
    "Як можна застосовувати штучний інтелект в бізнесі, щоб зробити процеси більш ефективними?",
    "Як можна застосовувати розподілені системи в бізнесі?",
    "Чи можливо створити програму, яка буде відповідати на всі можливі питання?",
    "Якби ви мали можливість змінити підходи до навчання в університеті, що б ви запропонували?",
    "Якби ви мали можливість створити програму, щоб вона допомогла вам в будь-якій ситуації, що б ви запрограмували?",
    "Як можна застосувати програмування в космічних дослідженнях?",
    "Як можна застосовувати програмування в медицині?",
    "Чи можливо створити програму, яка зможе передбачити майбутнє?",
    "Як можна застосовувати програмування в мистецтві?",
    "Якби ви мали можливість створити робота-музиканта, що б він вмів грати на інструменті?",
    "Як можна використовувати штучний інтелект в економіці?",
    "Як можна створити програму, яка буде керувати всіма діями у вашому житті?",
    "Як можна використовувати програмування для створення нових видів музики?",
    "Якби ви мали можливість вплинути на розвиток комп'ютерної техніки, що б ви змінили?"
]

past_life = [
    "Чаклун",
    "Гравець на бубнах",
    "Ілюзіоніст",
    "Скаут",
    "Організатор пікніків",
    "Співак операційної сестри",
    "Масажист",
    "Велосипедист",
    "Штурман корабля-вітрильника",
    "Художник з воску",
    "Пастух",
    "Оператор знімальної групи",
    "Розповідач казок",
    "Верхова єздачка на слонах",
    "Танцівник з табуретками",
    "Організатор плавань по рікам",
    "Акробат на коні",
    "Корабельний кок",
    "Палеонтолог-геолог",
    "Пірат",
    "Монах",
    "Суперник Робін Гуда",
    "Вершник на візках з бегоньками",
    "Бармен",
    "Майстер з гончарства",
    "Волоцюга-бродяга",
    "Хімік-алхімік",
    "Булочник",
    "Фермер-скотар",
    "Мандрівний торговець",
    "Водопровідник для мурашок.",
    "Людина, яка перевіряла товщину льоду на океані за допомогою зубної щітки.",
    "Професійний катальник по снігу на вуличних лопатах.",
    "Розмовний попугай, який говорив тільки на іншій мові.",
    "Координатор снігових бурь у пустелі.",
    "Експерт з визначення кольору диму.",
    "Дослідник ефекту духовки на рослини.",
    "Інструктор по миттю невмивних вікон.",
    "Майстер карате, який вміє бити тільки рибою.",
    "Дослідник глибин океану за допомогою підводної бритви.",
    "Професійний варильник яєць з одним оком.",
    "Астронавт, який керував космічними кораблями на зворотньому ходу.",
    "Танцівник бальних танців для ескімосів.",
    "Ремонтник підводних кабелів з використанням зубних ниток.",
    "Експерт з вивчення барвника шафрану у кішечках.",
]

def inline_answers(query: str):
    percentrage = random.randint(0, 100)
    heart = ("💔", "❤️‍🩹", "💜", "💖", "❤️‍🔥")[percentrage//25]
    part_live_text = random.choice(past_life)
    ideology = random.choice(ideologies)
    exercise = random.choice(spots_exercises)
    count_of_exercises = random.randint(5, 50)
    topic = random.choice(topics)
    return {
        "love" : f"Ви й {query} підходите друг другу на {heart} {percentrage}% {heart}",
        "past_live" : f"В минулому житті ти був {part_live_text}",
        "ideology" : f"Твоя політична ідеологія: {ideology}",
        "exercises" : f"{exercise} {count_of_exercises} разів!",
        "topic" : topic
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
        if i == 11: result += "\n"
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
    filepath = "data/random_day.json"
    def __init__(self):
        file = open(self.filepath, "r", encoding="utf-8") 
        self.textlist = json.load(file)

    def format_text(self, users: list[Users]) -> Tuple[str, int, list[Users]]:
        text_id = random.randrange(0, len(self.textlist))
        format_text = self.textlist[text_id]
        users = random.choices(users, k=format_text["n_users"])
        usernames = [user.username for user in users]
        return format_text["text"].format(*usernames), text_id, users
    
    def format_text_by_text_id(self, users: list[Users], text_id) -> str:
        usernames = [user.username for user in users]
        text = self.textlist[text_id]
        n_users = text["n_users"]
        while len(usernames) < n_users:
            usernames.append(usernames[-1])
        return text["text"].format(*usernames)

format_random_day = FormatRandomDay()