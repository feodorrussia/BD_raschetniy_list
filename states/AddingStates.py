from aiogram.dispatcher.filters.state import State, StatesGroup

class AddEmployee(StatesGroup):
    name = State()
    date_hire = State()
    gender = State()
    children = State()

class AddChild(StatesGroup):
    name_employee = State()
    birthday = State()

class AddContact(StatesGroup):
    descr = State()

class AddPosition(StatesGroup):
    descr = State()

class AddAward(StatesGroup):
    type = State()

class AddAwardToEmployee(StatesGroup):
    name_employee = State()