from aiogram.dispatcher.filters.state import State, StatesGroup

class AddEmployee(StatesGroup):
    name = State()
    date_hire = State()
    gender = State()
    children = State()

class AddChild(StatesGroup):
    name_employee = State()
    birthday = State()

class AddContract(StatesGroup):
    descr = State()
    type = State()
    date_start = State()
    date_end = State()

class AddPosition(StatesGroup):
    descr = State()
    wage = State()
    num_stuff = State()

class AddAward(StatesGroup):
    type = State()
    descr = State()
    cost = State()

class AddAwardToEmployee(StatesGroup):
    name_employee = State()