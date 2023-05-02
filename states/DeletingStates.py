from aiogram.dispatcher.filters.state import State, StatesGroup

class FireEmployee(StatesGroup):
    name_employee = State()
    date_fire = State()

class DeleteContract(StatesGroup):
    name = State()
    check = State()

class DeleteChild(StatesGroup):
    name_employee = State()
    date = State()

class DeleteAward(StatesGroup):
    type = State()
    name = State()
    check = State()

class DeletePosition(StatesGroup):
    name = State()
    check = State()
