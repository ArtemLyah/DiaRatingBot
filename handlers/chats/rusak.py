from aiogram import Router
from aiogram import filters, types
from keyboards.inline import rusak_keyboard
from keyboards.inline.callback_datas import RusakData
from services import RusakService
from data import text
import random

rusak_router = Router()
rusak_service = RusakService()

@rusak_router.message(filters.Command("donbass"))
async def donbass(message: types.Message):
    user = message.from_user
    if await rusak_service.get_rusak(user.id):
        await message.reply("У вас вже є русак")
        return
    await message.answer("Донбас - чудове місце для того щоб впіймати русака", reply_markup=rusak_keyboard(user.id))

@rusak_router.callback_query(RusakData.filter())
async def create_rusak(
    callback: types.CallbackQuery,
    callback_data: RusakData
):
    user = callback.from_user
    if str(user.id) != callback_data.user_id:
        return

    await callback.message.delete()
    if random.randint(1, 100) < 40:
        await callback.message.answer("Русак втік від вас")
        return
    rusak, photo_url = await rusak_service.add_rusak(user.id)    
    await callback.message.answer_photo(
        photo=photo_url,
        caption=text.rusak_info(
            user.full_name,
            rusak.name, 
            rusak.intellect, 
            rusak.strength, 
            rusak.rashism, 
            rusak.health
        )
    )

@rusak_router.message(filters.Command("rusak"))
async def get_rusak(message: types.Message):
    user = message.from_user

    rusak_info = await rusak_service.get_rusak(user.id)
    if not rusak_info:
        await message.reply("У вас не має русака")
        return

    rusak, photo_url = rusak_info
    await message.reply_photo(
        photo=photo_url,
        caption=text.rusak_info(
            user.full_name,
            rusak.name, 
            rusak.intellect, 
            rusak.strength, 
            rusak.rashism, 
            rusak.health
        )
    )

@rusak_router.message(filters.Command("kill_rusak"))
async def delete_rusak(message: types.Message):
    user = message.from_user
    rusak_name = rusak_service.delete_rusak(user.id)
    await message.reply(f'{rusak_name} був убитий.\nНове м\'ясо на борщ')

@rusak_router.message(filters.Command("compare_rusak"))
async def compare_rusak(message: types.Message):
    user = message.from_user
    if not message.reply_to_message:
        await message.reply("Зробіть (reply) на повідомлення людини з якою бажаєте порівняти русаків")
        return 
        
    reply_user = message.reply_to_message.from_user
    user_rusak = await rusak_service.get_rusak(user.id)
    reply_rusak = await rusak_service.get_rusak(reply_user.id)

    if not user_rusak:
        await message.reply("У вас не має русака")
        return
    if not reply_rusak:
        await message.answer(f"{reply_user.full_name} не має русака")
        return

    user_rusak = user_rusak[0]
    reply_rusak = reply_rusak[0]

    if not user_rusak:
        await message.reply("У вас не має русака")
    elif not reply_rusak:
        await message.reply(f"{reply_user.full_name} не має русака")
    else:
        await message.reply(text.format_comparing_rusak(user_rusak, reply_rusak))
