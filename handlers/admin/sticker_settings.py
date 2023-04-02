from aiogram import Router, filters, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_type import ChatType
from filters import IsAdminFilter, ChatTypeFilter
from state.admin_states import AddMark, DeleteMark
from services.sticker_service import StickerService
import json

sticker_settings_router = Router()
sticker_settings_router.message.filter(IsAdminFilter(), ChatTypeFilter(ChatType.PRIVATE))

sticker_service = StickerService()

################ ADD STICKER ################

@sticker_settings_router.message(filters.Command("add_sticker"))
async def add_sticker(message: types.Message, state:FSMContext):
    await message.answer("Send sticker")
    await state.set_state(AddMark.addSticker)

@sticker_settings_router.message(F.sticker, AddMark.addSticker)
async def save_sticker(message: types.Message, state:FSMContext):
    sticker_file_id = message.sticker.file_unique_id

    if sticker_service.is_sticker_in_set(sticker_file_id):
        await message.answer("Sticker is already in set")
        await state.clear()
        return

    await state.set_data({
        "file_id" : sticker_file_id
    })
    await message.answer("Now send the rating")
    await state.set_state(AddMark.addRating)

@sticker_settings_router.message(F.text, AddMark.addRating)
async def add_rating(message: types.Message, state:FSMContext):
    data = await state.get_data()
    sticker = {
        "file_id" : data["file_id"],
        "rating" : int(message.text)
    }
    sticker_service.add_sticker(**sticker)
    await message.answer("Sticker was added:\n"+json.dumps(sticker, indent=2))
    await state.clear()

################ DELETE STICKER ################

@sticker_settings_router.message(filters.Command("delete_sticker"))
async def delete_sticker_command(message: types.Message, state: FSMContext):
    await message.answer("Send the sticker to delete")
    await state.set_state(DeleteMark.deleteSticker)

@sticker_settings_router.message(F.sticker, DeleteMark.deleteSticker)
async def delete_sticker(message: types.Message, state: FSMContext):
    sticker_file_id = message.sticker.file_unique_id
    if sticker_service.is_sticker_in_set(sticker_file_id):
        sticker_service.delete_sticker(sticker_file_id)
        await message.answer("Sticker was successfully deleted")
        await state.clear()
    else:
        await message.answer("This sticker isn't in set")