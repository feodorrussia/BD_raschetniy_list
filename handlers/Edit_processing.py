from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.DeletingStates import *
from states.AdminStatus import AdminStatus


async def fire_employee_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await FireEmployee.name_employee.set()
    await call.message.answer("Введите ФИО уволенного сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def end_contract_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await EndContract.name.set()
    await call.message.answer("Введите название контракта, который хотите закончить",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def delete_child_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteChild.name_employee.set()

    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def delete_award_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteAward.type.set()
    await call.message.answer("Введите тип (поощрение/штраф)", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def delete_position_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeletePosition.name.set()
    await call.message.answer("Введите название должности", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def delete_award_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteAward.type.set()
    await call.message.answer("Введите тип (поощрение/штраф)", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def delete_position_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeletePosition.name.set()
    await call.message.answer("Введите название должности", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


def register_handlers_edit(dp: Dispatcher):
    dp.register_callback_query_handler(fire_employee_handler, lambda call: call.data == "edit_employee",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(end_contract_handler, lambda call: call.data == "edit_child",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(delete_child_handler, lambda call: call.data == "edit_rate",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(delete_award_handler, lambda call: call.data == "edit_contract",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(delete_position_handler, lambda call: call.data == "edit_position",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(delete_award_handler, lambda call: call.data == "edit_award",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(delete_position_handler, lambda call: call.data == "edit_award_employee",
                                       state=AdminStatus.authorized)
