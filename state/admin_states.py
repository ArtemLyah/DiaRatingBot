from aiogram.fsm.state import StatesGroup, State

class AddMark(StatesGroup):
    addSticker = State()
    addRating = State()

class DeleteMark(StatesGroup):
    deleteSticker = State()