from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.DeletingStates import *
from states.AdminStatus import AdminStatus


async def edit_employee_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await FireEmployee.name_employee.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def edit_child_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteChild.name_employee.set()

    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def edit_rate_employee_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteAward.type.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def edit_contract_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteContract.name.set()
    await call.message.answer("Введите название контракта, который хотите изменить",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def edit_position_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeletePosition.name.set()
    await call.message.answer("Введите название должности", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def edit_award_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteAward.type.set()
    await call.message.answer("Введите тип (поощрение/штраф)", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def edit_award_employee_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeletePosition.name.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


def register_handlers_edit(dp: Dispatcher):
    dp.register_callback_query_handler(edit_employee_handler, lambda call: call.data == "edit_employee",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(edit_child_handler, lambda call: call.data == "edit_child",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(edit_rate_employee_handler, lambda call: call.data == "edit_rate",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(edit_contract_handler , lambda call: call.data == "edit_contract",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(edit_position_handler, lambda call: call.data == "edit_position",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(edit_award_handler, lambda call: call.data == "edit_award",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(edit_award_employee_handler, lambda call: call.data == "edit_award_employee",
                                       state=AdminStatus.authorized)
