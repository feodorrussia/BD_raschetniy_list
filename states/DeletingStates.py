from aiogram.dispatcher.filters.state import State, StatesGroup

class FireEmployee(StatesGroup):
    name_employee = State()
    date_fire = State()