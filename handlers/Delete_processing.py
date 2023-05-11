from aiogram import types, Dispatcher
from create_bot import *
from other.functions import *
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.DeletingStates import *
from states.AdminStatus import AdminStatus
import json


async def fire_employee_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await FireEmployee.name_employee.set()
    await call.message.answer("Введите ФИО уволенного сотрудника\nСписок сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_fire_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)

        name = message.text.strip().split()
        employees = session.query(Employee).filter_by(firstname=name[0], lastname=name[1]).all()
        if len(employees) > 0:
            data[f"{chat_id}_edit_employee"] = {"employee_id": employees[0].id}
        else:
            await bot.send_message(chat_id, "Сотрудник не найден. Введите ФИО сотрудника\n" +
                                   "Список сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
            return
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    await FireEmployee.next()
    await bot.send_message(chat_id,
                           "Введите дату увольнения сотрудника\n(если сотрудник уволен сегодня, то введите сегодняшнюю дату)",
                           reply_markup=types.ReplyKeyboardRemove())


async def date_fire_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    if check_date(message.text.strip()):
        with open(data_name_file, "r+") as file:
            data = json.load(file)
            date = list(map(int, message.text.split('.')))

            employee = session.query(Employee).filter_by(id=data[f"{chat_id}_edit_employee"]["employee_id"]).first()
            difference_date = dif_date(employee.date_hired, datetime.date(date[2], date[1], date[0]))
            if difference_date[0] < 0 or difference_date[0] < 0 or difference_date[0] < 0:
                await bot.send_message(chat_id,
                                       f"Дата введена не правильно. Сотрудник ещё не был нанят в это время. Введите дату позже дня приёма на работу",
                                       reply_markup=types.ReplyKeyboardRemove())
                return

            date_fire = datetime.date(date[2], date[1], date[0])
            employee.date_fired = date_fire
            session.add(employee)
            session.commit()

            del (data[f"{chat_id}_edit_employee"])
            file.close()
        with open(data_name_file, "w") as file:
            json.dump(data, file, indent=4)
    else:
        await bot.send_message(chat_id, f"Дата введена не правильно. {date_rules()}Введите дату увольнения",
                               reply_markup=types.ReplyKeyboardRemove())

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_employee")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Принято. Хотите уволить ещё одного сотрудника?\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


def register_handlers_delete(dp: Dispatcher):
    dp.register_callback_query_handler(fire_employee_handler, lambda call: call.data == "del_employee",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_employee_fire_handler, state=FireEmployee.name_employee)
    dp.register_message_handler(date_fire_handler, state=FireEmployee.date_fire)