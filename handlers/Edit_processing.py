from aiogram import types, Dispatcher
from create_bot import *
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.EditingStates import *
from states.AdminStatus import AdminStatus
import json


async def edit_rate_employee_handler(call: types.CallbackQuery, state: FSMContext):  # Important!!!
    # await remove_chat_buttons(chat_id)
    await EditRate.name_employee.set()
    await call.message.answer("Введите ФИО сотрудника\nСписок сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_rate_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    name = message.text.strip().split()
    employees = session.query(Employee).filter_by(firstname=name[0], lastname=name[1]).all()
    if len(employees) > 0:
        rates_employee = session.query(Rate).filter_by(id_employee=employees[0].id).all()
        rates = []
        for rate_employee in rates_employee:
            position = session.query(Position).filter_by(id=rate_employee.id_position).first()
            contract_id = session.query(PosContr).filter_by(id_position=position.id).first().id
            contract = session.query(Contract).filter_by(id=contract_id).first()
            if contract.get_status():
                rates.append([rate_employee.id, f"{position.name} - {rate_employee.rate*100}% ({position.wage * rate_employee.rate} р.)"])
    else:
        await bot.send_message(chat_id, "Сотрудник не найден. Введите ФИО сотрудника\n" +
                               "Список сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
        return

    if len(rates) == 0:
        await bot.send_message(chat_id, "Сотрудник не имеет активных контрактов. Хотите добавить?", reply_markup=types.ReplyKeyboardRemove())
        return


    kb_rates = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    butts = [types.InlineKeyboardButton(text=rate[1], callback_data=f"edit_rate_{rate[0]}") for rate in rates]
    kb_rates.add(*butts)

    await EditRate.next()

    await bot.send_message(chat_id, f"Выберите должность, ставку которой хотите изменить",
                           reply_markup=kb_rates)


async def position_rate_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        id_rate = call.data.split("_")[-1]
        data[f"{chat_id}_edit_rate"] = {"rate_id": id_rate}
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    await EditRate.next()

    await bot.send_message(chat_id,
                           f"Введите новую ставку в процентах (целое число)",
                           reply_markup=types.ReplyKeyboardRemove())


async def update_rate_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        try:
            data[f"{chat_id}_edit_rate"]["rate"] = int(message.text.strip())/100
        except Exception as e:
            await bot.send_message(chat_id, "Ставка введена неверно. Введите новую ставку в процентах (целое число)",
                                   reply_markup=types.ReplyKeyboardRemove())
            return

        rate_id = data[f"{chat_id}_edit_rate"]["rate_id"]
        value = data[f"{chat_id}_edit_rate"]["rate"]
        rate_employee = session.query(Rate).filter_by(id=rate_id).first()
        rate_employee.rate = value
        session.add(rate_employee)
        session.commit()

        del(data[f"{chat_id}_edit_rate"])
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

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
