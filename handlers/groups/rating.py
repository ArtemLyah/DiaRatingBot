from aiogram import Router, types, filters, F
from aiogram.enums.chat_type import ChatType
from aiogram.handlers import MessageHandler
from services import RatingService, UserService, CountingsService
from databases import Users, UserGroup, Countings
from middlewares.rating_mw import StickerRatingMiddleware
from filters import ChatTypeFilter
from config import ADMINS
from datetime import datetime
from data import text

rating_router = Router()
rating_router.message.filter(ChatTypeFilter((ChatType.GROUP, ChatType.SUPERGROUP)))
rating_router.message.outer_middleware(StickerRatingMiddleware())

user_service = UserService()
rating_service = RatingService()
counting_service = CountingsService()


@rating_router.message(F.sticker, F.reply_to_message)
async def addRating(message: types.Message, rating: int, db_userGroup: UserGroup, db_counting: Countings):
    if db_userGroup.is_ban:
            return
    if rating is None:
        return

    group = message.chat
    user = message.from_user
    reply_user = message.reply_to_message.from_user
    user_service.addUser(reply_user.id, reply_user.full_name, reply_user.username)
    db_reply_userGroup = user_service.addUserGroup(group.id, reply_user.id)

    if user.id == reply_user.id and not user.id in ADMINS:
        await message.reply("Хей! Ви не можене повисити чи понизити свій рейтинг!")
        return
    
    limit_raiting = rating_service.calculateLimit(user_id=user.id)
    update_limit_date = db_counting.update_limit_date
    new_count_rating = db_counting.count_rating + abs(rating)

    if datetime.now().date() >= update_limit_date:
        counting_service.resetCountings(user.id, count_rating=abs(rating))
    elif new_count_rating > limit_raiting:
        await message.reply("Ваш щоденний ліміт на дія.бали вичерпався")
        return 
    else:
        counting_service.updateCounting(
            Countings.count_rating, 
            user.id, 
            new_count_rating
        )
    
    rating = rating_service.addRating(db_reply_userGroup, rating)
    emoji = message.sticker.emoji
    await message.reply(text.format_status(f"{emoji} Дія.рейтинг у {reply_user.full_name} тепер становить {rating}", rating)) 
        
@rating_router.message(filters.Command("present"))
class PresentHandler(MessageHandler):
    async def __parse_commands(self, commands):
        try:
            if len(commands) == 1 and self.event.reply_to_message:
                reply_user = self.event.reply_to_message.from_user
                rating = int(commands[0])
            elif len(commands) == 2:
                reply_user = user_service.getUserByUsername(commands[0][1:])
                rating = int(commands[1])
            else:
                await self.event.reply("Команда не вірна. Зробіть (reply) на повідомлення, далі /present й кількість балів які бажаєте подарувати")
                return None
        except ValueError:
            await self.event.reply("Невірно вказано кількість балів")
            return None
        return reply_user, rating

    async def handle(self):
        commands = self.event.text.split()[1:]
        group_id = self.event.chat.id
        user = self.event.from_user
        db_userGroup: UserGroup = self.data["db_userGroup"] 
        db_counting: Countings = self.data["db_counting"]
        
        if db_userGroup.is_ban:
            return

        commands = await self.__parse_commands(commands)
        if commands is None:
            return

        reply_user, rating = commands
        user_service.addUser(reply_user.id, reply_user.full_name, reply_user.username)
        reply_userGroup = user_service.addUserGroup(group_id, reply_user.id)

        if datetime.now().date() >= db_counting.update_limit_date:
            counting_service.resetCountings(user.id, count_rating=abs(rating))
        if user.id == reply_user.id:
            await self.event.reply("Ви не можете дарувати самому собі дія.бали")
            return
        elif rating <= 0:
            await self.event.reply("Ви не можете подарувати від'ємні дія.бали")
            return
        elif db_counting.count_present+rating > db_userGroup.local_rating // 3:
            await self.event.reply("Ваш щоденний ліміт на подарунок дія.балів вичерпався")
            return
        else:
            counting_service.updateCounting(
                Countings.count_present, 
                user.id, 
                db_counting.count_present+rating
            )
            user_rating = rating_service.addRating(db_userGroup, -rating)
            reply_user_rating = rating_service.addRating(reply_userGroup, rating)
            await self.event.reply(f"{user.full_name} подарував/ла {rating} дія.балів для {reply_user.full_name}")
            await self.event.answer(f"Рейтинг у {user.full_name} тепер становить {user_rating}")
            await self.event.answer(text.format_status(f"Рейтинг у {reply_user.full_name} тепер становить {reply_user_rating}", reply_user_rating))