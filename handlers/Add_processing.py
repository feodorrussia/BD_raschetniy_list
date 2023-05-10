from aiogram import types, Dispatcher
from create_bot import *
from other.functions import *
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.AddingStates import *
from states.AdminStatus import AdminStatus
import json


async def add_employee_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddEmployee.name.set()
    await call.message.answer("Введите ФИО нового сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        data[f"{chat_id}_add_employee"] = {"name": message.text.strip()}
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    with open(data_name_file, "w") as file:
        json.dump(data, file, ensure_ascii=True)
    await AddEmployee.next()
    await bot.send_message(chat_id,
                           "Введите дату найма нового сотрудника?\n(если сотрудник нанят сегодня, то введите, пожалуйста, сегодняшнюю дату)",
                           reply_markup=types.ReplyKeyboardRemove())


async def date_hire_employee_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    butts = [types.KeyboardButton("М"), types.KeyboardButton("Ж")]
    kb.add(*butts)

    if check_date(message.text.strip()):
        with open(data_name_file, "r+") as file:
            data = json.load(file)
            date = list(map(int, message.text.split('.')))
            data[f"{chat_id}_add_employee"]["date_hire"] = date
            # print(data[f"{chat_id}_add_employee"]["name"])
            file.close()
        with open(data_name_file, "w") as file:
            json.dump(data, file, indent=4)

        # await remove_chat_buttons(chat_id)
        await AddEmployee.next()
        await bot.send_message(chat_id, "Введите пол нового сотрудника: <b>М</b>/<b>Ж</b>", reply_markup=kb,
                               parse_mode="html")
    else:
        await bot.send_message(chat_id,
                               f"Дата введена не правильно. {date_rules()}Введите дату найма нового сотрудника\n(если сотрудник нанят сегодня, то введите, пожалуйста, сегодняшнюю дату)",
                               reply_markup=types.ReplyKeyboardRemove())


async def gender_employee_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        if message.text.strip() == "Ж":
            data[f"{chat_id}_add_employee"]["gender"] = True
        else:
            data[f"{chat_id}_add_employee"]["gender"] = False

        name = data[f"{chat_id}_add_employee"]["name"].strip().split()
        date_hire = data[f"{chat_id}_add_employee"]["date_hire"]
        gender = Gender.female if data[f"{chat_id}_add_employee"]["gender"] else Gender.male
        employee = Employee(firstname=name[0], lastname=name[1], middlename=None if len(name) < 3 else name[2],
                            gender=gender, date_hired=datetime.date(date_hire[2], date_hire[1], date_hire[0]))
        session.add(employee)
        session.commit()

        del (data[f"{chat_id}_add_employee"])
        file.close()

    data[f"{chat_id}_add_child"] = {"parent_id": session.query(Employee).filter_by(firstname=name[0], lastname=name[1],
                                                                                   date_hired=datetime.date(
                                                                                       date_hire[2],
                                                                                       date_hire[1],
                                                                                       date_hire[0]),
                                                                                   gender=gender).first().id}
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    await AddEmployee.next()
    await bot.send_message(chat_id,
                           "Введите дату рождения ребёнка нового сотрудника (чтобы закончить напишите <b>отмена</b>)",
                           parse_mode="html", reply_markup=types.ReplyKeyboardRemove())


async def children_employee_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    if check_date(message.text.strip()):
        with open(data_name_file, "r+") as file:
            data = json.load(file)
            employee_id = data[f"{chat_id}_add_child"]["parent_id"]

            date = list(map(int, message.text.split('.')))
            child = Child(id_employee=employee_id, birthday=datetime.date(date[2], date[1], date[0]))
            session.add(child)
            session.commit()
            file.close()

        if message.text == Text(equals="отмена", ignore_case=True):
            await state.finish()
            await AdminStatus.authorized.set()
        await bot.send_message(chat_id,
                               "Принято. Введите дату рождения ребёнка нового сотрудника (чтобы закончить напишите <b>отмена</b>)",
                               parse_mode="html", reply_markup=kb_cancel)
    else:
        await bot.send_message(chat_id,
                               f"Дата введена не правильно. {date_rules()}Введите дату рождения ребёнка нового сотрудника (чтобы закончить напишите <b>отмена</b>)",
                               reply_markup=kb_cancel)


async def add_child_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddChild.name_employee.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_parent_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        name = message.text.strip().split()
        employees = session.query(Employee).filter_by(firstname=name[0], lastname=name[1]).all()
        if len(employees) > 0:
            data[f"{chat_id}_add_child"] = {"parent_id": employees[0].id}
        else:
            await bot.send_message(chat_id, "Сотрудник не найден. Введите ФИО сотрудника\n" +
                                   "Список сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
            return
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    await AddChild.next()

    await bot.send_message(chat_id, "Сотрудник найден. Введите дату рождения ребёнка",
                           reply_markup=types.ReplyKeyboardRemove())


async def birthday_child_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    if check_date(message.text.strip()):
        with open(data_name_file, "r+") as file:
            data = json.load(file)
            employee_id = data[f"{chat_id}_add_child"]["parent_id"]

            date = list(map(int, message.text.split('.')))
            child = Child(id_employee=employee_id, birthday=datetime.date(date[2], date[1], date[0]))
            session.add(child)
            session.commit()
            file.close()

        kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
        butts = types.InlineKeyboardButton(text="Продолжить", callback_data="add_child")
        kb_continue.add(butts)

        await state.finish()
        await AdminStatus.authorized.set()

        await bot.send_message(chat_id, "Принято. Хотите добавить ещё одного ребёнка?" +
                               "\nМеню - /start_menu" +
                               "\nМеню добавления - /add_menu" +
                               "\nМеню удаления - /del_menu" +
                               "\nМеню изменения - /upd_menu" +
                               "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)
    else:
        await bot.send_message(chat_id, f"Дата введена не правильно. {date_rules()}Введите дату рождения ребёнка",
                               reply_markup=types.ReplyKeyboardRemove())


async def add_contract_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddContract.name.set()
    await call.message.answer("Введите название контракта", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_contract_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        data[f"{chat_id}_add_contract"] = {"name": message.text.strip()}
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    kb_type_contract = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butts = [types.KeyboardButton("основной"), types.KeyboardButton("дополнительный")]
    kb_type_contract.add(*butts)

    await AddContract.next()

    await bot.send_message(chat_id, "Введите тип контракта: <b>основной</b>/<b>дополнительный</b>)", parse_mode="html",
                           reply_markup=kb_type_contract)


async def type_contract_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        if message.text.strip().lower() == "основной":
            data[f"{chat_id}_add_contract"]["type"] = True
        else:
            data[f"{chat_id}_add_contract"]["type"] = False
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    await AddContract.next()

    await bot.send_message(chat_id, "Введите дату начала контракта", reply_markup=types.ReplyKeyboardRemove())


async def start_contract_date_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    if check_date(message.text.strip()):
        with open(data_name_file, "r+") as file:
            data = json.load(file)
            date = list(map(int, message.text.split('.')))
            data[f"{chat_id}_add_contract"]["date_start"] = date
            file.close()
        with open(data_name_file, "w") as file:
            json.dump(data, file, indent=4)

        await AddContract.next()
        await bot.send_message(chat_id, "Введите дату окончания контракта (она должна быть больше даты начала)",
                               reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(chat_id, f"Дата введена не правильно. {date_rules()}Введите дату начала контракта",
                               reply_markup=types.ReplyKeyboardRemove())


async def end_contract_date_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    if check_date(message.text.strip()):
        with open(data_name_file, "r+") as file:
            data = json.load(file)
            date = list(map(int, message.text.split('.')))
            data[f"{chat_id}_add_contract"]["date_end"] = date

            name = data[f"{chat_id}_add_contract"]["name"].strip()
            date_start = data[f"{chat_id}_add_contract"]["date_start"]
            date_start = datetime.date(date_start[2], date_start[1], date_start[0])
            date_end = data[f"{chat_id}_add_contract"]["date_end"]
            date_end = datetime.date(date_end[2], date_end[1], date_end[0])

            duration = dif_date(date_start, date_end)
            if duration[0] < 0 or duration[1] < 0 or duration[2] < 0:
                await bot.send_message(chat_id,
                                       f"Дата введена не правильно. {date_rules()}Введите дату окончания контракта (она должна быть больше даты начала)",
                                       reply_markup=types.ReplyKeyboardRemove())
                return

            type_c = ContractTypes.main if data[f"{chat_id}_add_contract"]["type"] else ContractTypes.addition
            contract = Contract(name=name, type=type_c, start_date=date_start, end_date=date_end)
            session.add(contract)
            session.commit()

            del (data[f"{chat_id}_add_contract"])
            file.close()
        with open(data_name_file, "w") as file:
            json.dump(data, file, indent=4)

        kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
        butts = types.InlineKeyboardButton(text="Продолжить", callback_data="add_contract")
        kb_continue.add(butts)

        await state.finish()
        await AdminStatus.authorized.set()

        await bot.send_message(chat_id, "Принято. Хотите добавить ещё один контракт?\nМеню - /start_menu" +
                               "\nМеню добавления - /add_menu" +
                               "\nМеню удаления - /del_menu" +
                               "\nМеню изменения - /upd_menu" +
                               "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)
    else:
        await bot.send_message(chat_id, f"Дата введена не правильно. {date_rules()}Введите дату окончания контракта",
                               reply_markup=types.ReplyKeyboardRemove())


async def add_employee_to_position_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddEmployeeToContract.name_employee.set()
    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_position_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        name = message.text.strip().split()
        employees = session.query(Employee).filter_by(firstname=name[0], lastname=name[1]).all()
        if len(employees) > 0:
            data[f"{chat_id}_add_position_to_employee"] = {"employee_id": employees[0].id}
        else:
            await bot.send_message(chat_id, "Сотрудник не найден. Введите ФИО сотрудника\n" +
                                   "Список сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
            return
        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)

    await AddEmployeeToContract.next()

    await bot.send_message(chat_id, "Введите название контракта",
                           reply_markup=types.ReplyKeyboardRemove())


async def name_contract_employee_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(data_name_file, "r+") as file:
        data = json.load(file)
        name = message.text.strip()
        contracts = session.query(Contract).filter_by(name=name).all()
        if len(contracts) > 0:
            data[f"{chat_id}_add_position_to_employee"] = {"contract_id": contracts[0].id}
        else:
            await bot.send_message(chat_id, "Контракт не найден. Введите название контракта\n" +
                                   "Список контрактов - /contracts", reply_markup=types.ReplyKeyboardRemove())
            return

        vacancy = [[1, "Programming - 2"], [2, "Math - 1"], [3, "Data engineer - 1"]]
        # vacancy = session.query(PosContr).filter_by(id_contract=contracts[0].id)

        file.close()
    with open(data_name_file, "w") as file:
        json.dump(data, file, indent=4)



    kb_vacancies = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    butts = [types.InlineKeyboardButton(text=rate[1], callback_data=f"add_position_{rate[0]}") for rate in vacancy]
    kb_vacancies.add(*butts)

    await AddEmployeeToContract.next()

    await bot.send_message(chat_id, "Введите позицию для сотруднику",
                           reply_markup=kb_vacancies)


async def name_position_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddEmployeeToContract.next()

    await bot.send_message(chat_id, "Введите ставку сотрудника",
                           reply_markup=types.ReplyKeyboardRemove())


async def wage_employee_position_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="add_position")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Принято. Хотите назначить сотрудника на ещё одну должность?\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def add_position_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddPosition.name.set()
    await call.message.answer("Введите название должности", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_position_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddPosition.next()

    await bot.send_message(chat_id, "Введите контракт этой должности",
                           reply_markup=types.ReplyKeyboardRemove())


async def contract_position_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddPosition.next()

    await bot.send_message(chat_id, "Введите зарплату сотрудника на этой должности",
                           reply_markup=types.ReplyKeyboardRemove())


async def wage_position_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddPosition.next()

    await bot.send_message(chat_id,
                           "Введите количество человек, необходимых на этой должности (количество полных ставок)",
                           reply_markup=types.ReplyKeyboardRemove())


async def number_stuff_position_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="add_position")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Принято. Хотите добавить ещё одну должность?\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def add_award_handler(call: types.CallbackQuery, state: FSMContext):
    kb_award = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butts = [types.KeyboardButton("Поощрение"), types.KeyboardButton("Штраф")]
    kb_award.add(*butts)

    # await remove_chat_buttons(chat_id)
    await AddAward.type.set()
    await call.message.answer("Введите тип (поощрение/штраф)", reply_markup=kb_award)
    await call.answer()


async def type_award_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddAward.next()

    await bot.send_message(chat_id, f"Введите описание {'поощрения' if True else 'штрафа'}",
                           reply_markup=types.ReplyKeyboardRemove())


async def name_award_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddAward.next()

    await bot.send_message(chat_id, f"Введите сумму {'поощрения' if True else 'штрафа'}",
                           reply_markup=types.ReplyKeyboardRemove())


async def award_cost_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="add_award")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Принято. Хотите добавить ещё одно поощрение/штраф?\nМеню - /start_menu",
                           reply_markup=kb_continue)


async def add_award_to_employee_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await AddAwardToEmployee.name_employee.set()
    await call.message.answer(f"Введите ФИО сотрудника\n{'список сотрудников'}",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_to_award_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddAwardToEmployee.next()

    await bot.send_message(chat_id, f"Введите название поощрения/штрафа\n{'список поощрений/штрафов'}",
                           reply_markup=types.ReplyKeyboardRemove())


async def name_award_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await AddAwardToEmployee.next()

    await bot.send_message(chat_id, "Введите дату назначения поощрения/штрафа",
                           reply_markup=types.ReplyKeyboardRemove())


async def date_award_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="add_award_to_employee")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id,
                           "Принято. Хотите назначить ещё одно поощрение/штраф сотруднику?\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


def register_handlers_add(dp: Dispatcher):
    dp.register_callback_query_handler(add_employee_handler, lambda call: call.data == "add_employee",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_employee_handler, state=AddEmployee.name)
    dp.register_message_handler(date_hire_employee_handler, state=AddEmployee.date_hire)
    dp.register_message_handler(gender_employee_handler, state=AddEmployee.gender)
    dp.register_message_handler(children_employee_handler, state=AddEmployee.children)

    dp.register_callback_query_handler(add_child_handler, lambda call: call.data == "add_child",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_parent_handler, state=AddChild.name_employee)
    dp.register_message_handler(birthday_child_handler, state=AddChild.birthday)

    dp.register_callback_query_handler(add_contract_handler, lambda call: call.data == "add_contract",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_contract_handler, state=AddContract.name)
    dp.register_message_handler(type_contract_handler, state=AddContract.type)
    dp.register_message_handler(start_contract_date_handler, state=AddContract.date_start)
    dp.register_message_handler(end_contract_date_handler, state=AddContract.date_end)

    dp.register_callback_query_handler(add_employee_to_position_handler,
                                       lambda call: call.data == "add_contract_to_employee",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_employee_position_handler, state=AddEmployeeToContract.name_employee)
    dp.register_message_handler(name_contract_employee_handler, state=AddEmployeeToContract.name_contract)
    dp.register_callback_query_handler(name_position_handler, state=AddEmployeeToContract.position)
    dp.register_message_handler(wage_employee_position_handler, state=AddEmployeeToContract.rate)

    dp.register_callback_query_handler(add_position_handler, lambda call: call.data == "add_position",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_position_handler, state=AddPosition.name)
    dp.register_message_handler(contract_position_handler, state=AddPosition.name_contract)
    dp.register_message_handler(wage_position_handler, state=AddPosition.wage)
    dp.register_message_handler(number_stuff_position_handler, state=AddPosition.num_stuff)

    dp.register_callback_query_handler(add_award_handler, lambda call: call.data == "add_award",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(type_award_handler, state=AddAward.type)
    dp.register_message_handler(name_award_handler, state=AddAward.name)
    dp.register_message_handler(award_cost_handler, state=AddAward.cost)

    dp.register_callback_query_handler(add_award_to_employee_handler, lambda call: call.data == "add_award_to_employee",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_employee_to_award_handler, state=AddAwardToEmployee.name_employee)
    dp.register_message_handler(name_award_handler, state=AddAwardToEmployee.name_award)
    dp.register_message_handler(date_award_handler, state=AddAwardToEmployee.date)
