from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminStatus(StatesGroup):
    unauthorized = State()
    authorizing = State()
    authorized = State()