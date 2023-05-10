from aiogram.dispatcher.filters.state import State, StatesGroup

class EditRate(StatesGroup):
    name_employee = State()
    position = State()
    new_value = State()