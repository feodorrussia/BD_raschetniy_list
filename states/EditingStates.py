from aiogram.dispatcher.filters.state import State, StatesGroup

class EditEmployee(StatesGroup):
    name_employee = State()


class EditChild(StatesGroup):
    name_employee = State()


class EditRate(StatesGroup):
    name_employee = State()
    position = State()
    new_value = State()


class EditContract(StatesGroup):
    name_contract = State()


class EditPosition(StatesGroup):
    name_position = State()


class EditAward(StatesGroup):
    type = State()
    name_award = State()


class EditAwardEmployee(StatesGroup):
    name_employee = State()