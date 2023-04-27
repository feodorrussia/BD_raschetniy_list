from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.AddingStates import *
from states.AdminStatus import AdminStatus


async def add_employee_handler(call: types.CallbackQuery, state : FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddEmployee.name.set()
    await call.message.answer("Введите ФИО нового сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_handler(message: types.Message, state : FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    await AddEmployee.next()
    await bot.send_message(chat_id, "Введите дату найма нового сотрудника?\n(если сотрудник нанят сегодня, то введите <b>now</b> или сегодняшнюю дату)", parse_mode="html", reply_markup=types.ReplyKeyboardRemove())


async def date_hire_employee_handler(message: types.Message, state : FSMContext):
    chat_id = message.chat.id

    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    butts = [types.KeyboardButton("М"), types.KeyboardButton("Ж")]
    kb.add(*butts)

    # await remove_chat_buttons(chat_id)
    await AddEmployee.next()
    await bot.send_message(chat_id, "Введите пол нового сотрудника: <b>М</b>/<b>Ж</b>", reply_markup=kb, parse_mode="html")


async def gender_employee_handler(message: types.Message, state : FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    await AddEmployee.next()
    await bot.send_message(chat_id, "Введите дату рождения ребёнка нового сотрудника (чтобы закончить напишите <b>отмена</b>)", parse_mode="html", reply_markup=types.ReplyKeyboardRemove())


async def children_employee_handler(message: types.Message, state : FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    if message.text == Text(equals="отмена", ignore_case=True):
        await state.finish()
        await AdminStatus.authorized.set()
    await bot.send_message(chat_id, "Принято. Введите дату рождения ребёнка нового сотрудника (чтобы закончить напишите <b>отмена</b>)", parse_mode="html", reply_markup=kb_cancel)


async def add_child_handler(call: types.CallbackQuery, state : FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddChild.name_employee.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def add_contract_handler(call: types.CallbackQuery, state : FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddContact.descr.set()
    await call.message.answer("Введите название контракта", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def add_position_handler(call: types.CallbackQuery, state : FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddPosition.descr.set()
    await call.message.answer("Введите название должности", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def add_award_handler(call: types.CallbackQuery, state : FSMContext):

    kb_award = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butts = [types.KeyboardButton("Поощрение"), types.KeyboardButton("Штраф")]
    kb_award.add(butts)

    # await remove_chat_buttons(chat_id)
    await AddAward.type.set()
    await call.message.answer("Введите тип (поощрение/штраф)", reply_markup=kb_award)
    await call.answer()


async def add_award_to_employee_handler(call: types.CallbackQuery, state : FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddAwardToEmployee.name_employee.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


def register_handlers_add(dp : Dispatcher):
    dp.register_callback_query_handler(add_employee_handler, lambda call: call.data == "add_employee", state="*")
    dp.register_message_handler(name_employee_handler, state=AddEmployee.name)
    dp.register_message_handler(date_hire_employee_handler, state=AddEmployee.date_hire)
    dp.register_message_handler(gender_employee_handler, state=AddEmployee.gender)
    dp.register_message_handler(children_employee_handler, state=AddEmployee.children)

    dp.register_callback_query_handler(add_child_handler, lambda call: call.data == "add_child", state=AdminStatus.authorized)

    dp.register_callback_query_handler(add_contract_handler, lambda call: call.data == "add_contract", state=AdminStatus.authorized)

    dp.register_callback_query_handler(add_position_handler, lambda call: call.data == "add_position", state=AdminStatus.authorized)

    dp.register_callback_query_handler(add_award_handler, lambda call: call.data == "add_award", state=AdminStatus.authorized)

    dp.register_callback_query_handler(add_award_to_employee_handler, lambda call: call.data == "add_award_to_employee", state=AdminStatus.authorized)

