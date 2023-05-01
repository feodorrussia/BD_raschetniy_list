from aiogram.dispatcher.filters.state import State, StatesGroup

class EditEmployee(StatesGroup):
    name_employee = State()


class EditChild(StatesGroup):
    name_employee = State()


class EditRate(StatesGroup):
    name_employee = State()


class EditPosition(StatesGroup):
    name_employee = State()


class EditAward(StatesGroup):
    name_employee = State()


class EditAwardEmployee(StatesGroup):
    name_employee = State()