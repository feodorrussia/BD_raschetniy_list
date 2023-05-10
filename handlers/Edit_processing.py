from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.EditingStates import *
from states.AdminStatus import AdminStatus


async def edit_rate_employee_handler(call: types.CallbackQuery, state: FSMContext):  # Important!!!
    # await remove_chat_buttons(chat_id)
    await EditRate.name_employee.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_rate_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    rates = [[1, "Programming - 100%"], [2, "Math - 50%"], [3, "Data engineer - 80%"]]

    kb_rates = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    butts = [types.InlineKeyboardButton(text=rate[1], callback_data=f"edit_rate_{rate[0]}") for rate in rates]
    kb_rates.add(*butts)

    await EditRate.next()

    await bot.send_message(chat_id, f"Выберите должность, ставку которой хотите изменить",
                           reply_markup=kb_rates)


async def position_rate_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    id_rate = call.data.split("_")[-1]
    # await remove_chat_buttons(chat_id)

    await EditRate.next()

    await bot.send_message(chat_id,
                           f"Ставка {id_rate} выбрана. Введите новую ставку",
                           reply_markup=types.ReplyKeyboardRemove())


async def update_rate_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_award")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Ставка обновлена. Желаете продолжить?" +
                           "\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


def register_handlers_edit(dp: Dispatcher):
    dp.register_callback_query_handler(edit_rate_employee_handler, lambda call: call.data == "edit_rate",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_employee_rate_handler, state=EditRate.name_employee)
    dp.register_callback_query_handler(position_rate_handler, state=EditRate.position)
    dp.register_message_handler(update_rate_handler, state=EditRate.new_value)
