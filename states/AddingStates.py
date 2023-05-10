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
    name = State()
    type = State()
    date_start = State()
    date_end = State()

class AddEmployeeToContract(StatesGroup):
    name_employee = State()
    name_contract = State()
    position = State()
    rate = State()

class AddPosition(StatesGroup):
    name = State()
    name_contract = State()
    wage = State()
    num_stuff = State()

class AddAward(StatesGroup):
    type = State()
    name = State()
    cost = State()

class AddAwardToEmployee(StatesGroup):
    name_employee = State()
    name_award = State()
    date = State()