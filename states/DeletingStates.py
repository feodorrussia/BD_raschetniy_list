from aiogram.dispatcher.filters.state import State, StatesGroup

class FireEmployee(StatesGroup):
    name_employee = State()
    date_fire = State()

class EndContract(StatesGroup):
    name = State()
    check = State()
    deleting = State()

class DeleteChild(StatesGroup):
    name_employee = State()
    check = State()
    deleting = State()

class DeleteAward(StatesGroup):
    name = State()
    check = State()
    deleting = State()

class DeletePosition(StatesGroup):
    name = State()
    check = State()
    deleting = State()
