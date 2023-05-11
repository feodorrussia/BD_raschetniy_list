from aiogram import types, Dispatcher
from create_bot import *
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.GeneratingStates import *
from states.AdminStatus import AdminStatus
from other.functions import *
from tabulate import tabulate


def list_vacancies_func():
    result = []
    positions = session.query(Position).all()
    for position in positions:
        contract_id = session.query(PosContr).filter_by(id_position=position.id).first().id_contract
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if contract.get_status():
            count = 1.5
            rates_employees = session.query(Rate).filter_by(id_position=position.id)
            for rate_position in list(filter(lambda x: x.id_position == position.id, rates_employees)):
                count -= rate_position.rate
            if count > 0:
                result.append([position.name, f"{count:.2f}", f"{position.wage:.2f} р."])
    text = tabulate(sorted(result, key=lambda x: x[0]), ["Название", "Ставок", "Зарплата"])
    return text


async def generate_list_vacancy_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    list_vacancies = list_vacancies_func()

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_vac")
    kb_doc.add(butt)

    await call.message.answer(f"Ваш список вакансий. Хотите получить список файлом?\n\n<code>{list_vacancies_func()}</code>", parse_mode="html", reply_markup=kb_doc)

    await call.message.answer("\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def generate_list_vacancy_doc_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    # await remove_chat_buttons(chat_id)
    list_vacancies = list_vacancies_func()

    with open(f"data/vacancy_{hash(chat_id)}.txt", "w") as file:
        file.write(f"Список вакансий\n\n{list_vacancies_func()}")
        file.close()

    with open(f"data/vacancy_{hash(chat_id)}.txt", "rb") as file:
        await bot.send_document(chat_id, file)
        file.close()

    await call.message.answer("Ваш файл:\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())

    await call.answer()

def cut_name(name: str, length: int = 35):
    if len(name) > length:
        return " ".join(name[:length-4].split())+"..."
    return name


def employee_profits_list_func(employee_id: int):
    profits = []
    count = 0

    contracts = []
    employee = session.query(Employee).filter_by(id=employee_id).first()
    rates_employee = session.query(Rate).filter_by(id_employee=employee_id).all()
    for rate_employee in rates_employee:
        position = session.query(Position).filter_by(id=rate_employee.id_position).first()
        contract_id = session.query(PosContr).filter_by(id_position=position.id).first().id_contract
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if contract.end_date > datetime.date(datetime.datetime.today().date().year, 1, 1):
            start_date = contract.start_date
            if contract.start_date < datetime.date(datetime.datetime.today().date().year, 1, 1):
                start_date = datetime.date(datetime.datetime.today().date().year, 1, 1)
            if contract.start_date < employee.date_hired:
                start_date = employee.date_hired
            days_in_work = (datetime.datetime.today().date() - start_date).days
            contracts.append([contract.name, contract.get_type(), rate_employee.rate, position.wage, days_in_work, f"{rate_employee.rate*position.wage/30*days_in_work:.2f} p."])
            count += rate_employee.rate*position.wage/30*days_in_work
    profits.append(contracts)

    awards = []
    penalties = []
    awards_employee = session.query(AwardEvent).filter_by(id_employee=employee_id).all()
    for award_employee in awards_employee:
        if award_employee.is_this_year():
            award = session.query(Award).filter_by(id=award_employee.id_award).first()
            if award.type == AwardTypes.award:
                awards.append([award.name, award.cost])
                count += award.cost
            else:
                penalties.append([award.name, award.cost])
                count -= award.cost
    profits.append(awards)
    profits.append(penalties)

    children = session.query(Child).filter_by(id_employee=employee_id).all()
    children_num = len(list(filter(lambda x: x.getAge() < 18, children)))
    taxes_minus = 0.13 - children_num * 0.03
    taxes = [0.13, children_num, taxes_minus if taxes_minus >= 0 else 0]
    profits.append(taxes)

    count_taxes = count
    if count > 0:
        count_taxes -= count*taxes[-1]
    profits.append(["Итого:", count, count_taxes])
    return profits


def list_profits():
    result = []
    count = 0
    employees = session.query(Employee).all()
    for employee in employees:
        count_employee = employee_profits_list_func(employee.id)[-1][-1]
        result.append([employee.get_name(), f"{count_employee:.2f} р."])
        count += count_employee
    result.sort(key=lambda x: -float(x[1].split()[0]))
    result.append(["------", f"{''.rjust(len(str(count))+3, '-')}"])
    result.append(["Итого:", f"{count:.2f} р."])

    text = tabulate(result, ["ФИО сотрудника", "Счёт за год с учётом налогов"])

    return text


async def generate_list_profits_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)

    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_list_profits")
    kb_doc.add(butt)

    await bot.send_message(call.message.chat.id, f"Итоговый расчётный лист сотрудников\n\n<code>{list_profits()}</code>", parse_mode="html", reply_markup=kb_doc)

    await call.message.answer("Ваш расчётный лист\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())

    await call.answer()


async def generate_doc_list_profits_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)

    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(f"data/profits_{hash(chat_id)}.txt", "w") as file:
        file.write(f"Итоговый расчётный лист сотрудников\n\n{list_profits()}")
        file.close()

    with open(f"data/profits_{hash(chat_id)}.txt", "rb") as file:
        await bot.send_document(chat_id, file)
        file.close()

    await call.message.answer("Ваш расчётный лист\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


def warnings_list():
    list_minus_employees = []
    list_contract_employees = []
    employees = session.query(Employee).all()
    for employee in employees:
        count_employee = employee_profits_list_func(employee.id)[-1][-1]
        if count_employee < 0:
            list_minus_employees.append(employee.get_name())

        rates_employee = session.query(Rate).filter_by(id=employee.id).all()
        flag_main_contarct = False
        for rate in rates_employee:
            position = session.query(Position).filter_by(id=rate.id_position).first()
            contract_id = session.query(PosContr).filter_by(id_position=position.id).first().id_contract
            contract = session.query(Contract).filter_by(id=contract_id).first()
            if contract.type == ContractTypes.main:
                if contract.get_status():
                    flag_main_contarct = True
        if not flag_main_contarct:
            list_contract_employees.append(employee.get_name())

    text = "Список предупреждений:\n\nИтоговый расчёт за месяц меньше нуля у следующих сотрудников:\n\n"
    if len(list_minus_employees) > 0:
        text += "\n".join([str(i + 1) + ". " + list_minus_employees[i] for i in range(len(list_minus_employees))])
    else:
        text += "Нет"

    text += "\n\nНе продлён основной контракт и сотрудник не уволен:\n\n"
    if len(list_contract_employees) > 0:
        text += "\n".join([str(i + 1) + ". " + list_contract_employees[i] for i in range(len(list_contract_employees))])
    else:
        text += "Нет"

    return text


async def generate_list_warning_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_warnings")
    kb_doc.add(butt)

    await call.message.answer(warnings_list(), reply_markup=kb_doc)

    await call.message.answer("\n\nМеню - /start_menu" +
        "\nМеню добавления - /add_menu" +
        "\nМеню удаления - /del_menu" +
        "\nМеню изменения - /upd_menu" +
        "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
        reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def generate_doc_warning_list_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)

    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(f"data/warnings_{hash(chat_id)}.txt", "w") as file:
        file.write(warnings_list())
        file.close()

    with open(f"data/warnings_{hash(chat_id)}.txt", "rb") as file:
        await bot.send_document(chat_id, file)
        file.close()

    await call.message.answer("Ваш файл с предупреждениями\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())

    await call.answer()


def employee_profit_list(employee_id: int):
    profit = employee_profits_list_func(employee_id)
    name = session.query(Employee).filter_by(id=employee_id).first().get_name()

    text = ""
    text += "\n\nКонтракты:\n"
    if len(profit[0]) > 0:
        text += tabulate(profit[0], ["Название", "Тип", "Ставка", "ЗП в месяц", "Работал дней", "Заработок за этот год"])
    else:
        text += "Нет."
    text += "\n\nПоощрения:\n"
    if len(profit[1]) > 0:
        text += tabulate(profit[1], ["Название", "Счёт"])
    else:
        text += "Нет."
    text += "\n\nШтрафы:\n"
    if len(profit[2]) > 0:
        text += tabulate(profit[2], ["Название", "Счёт"])
    else:
        text += "Нет."
    text += "\n\nНалоги и вычет:\n"
    text += tabulate([[profit[3][1], f"{profit[3][2]*100}%"]], ["Детей до 18", "Процент налогов с учётом вычета"]) + "\n\n"
    text += tabulate([[profit[-1][0], profit[-1][1], profit[-1][2]]], ["", "Счёт без учёта налогов", "Итоговый счёт"])

    return text


async def generate_list_employee_profit_handler(call: types.CallbackQuery):
    # await remove_chat_buttons(chat_id)
    await GenerateEmployeeProfit.name_employee.set()

    await call.message.answer("Введите ФИО сотрудника\nСписок сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def output_list_employee_profit_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    name = message.text.strip().split()
    employees = session.query(Employee).filter_by(firstname=name[0], lastname=name[1]).all()
    if len(employees) == 0:
        await bot.send_message(chat_id, "Сотрудник не найден. Введите ФИО сотрудника\n" +
                               "Список сотрудников - /employees", reply_markup=types.ReplyKeyboardRemove())
        return

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, f"Расчётный лист за год\nФИО: {' '.join(name)}\n\n<code>{employee_profit_list(employees[0].id)}</code>", parse_mode="html", reply_markup=types.ReplyKeyboardRemove())

    with open(f"data/employee_profit_{hash(chat_id)}.txt", "w") as file:
        file.write(f"Расчётный лист за год\nФИО: {' '.join(name)}\n\n{employee_profit_list(employees[0].id)}")
        file.close()

    with open(f"data/employee_profit_{hash(chat_id)}.txt", "rb") as file:
        await bot.send_document(chat_id, file)
        file.close()

    await bot.send_message(chat_id, f"Меню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())


async def generate_employee_list_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    employees = session.query(Employee).all()

    await call.message.answer(generate_employee_list(employees))
    await call.message.answer("\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def generate_employee_list_message_handler(message: types.Message, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    employees = session.query(Employee).all()

    await bot.send_message(message.chat.id, generate_employee_list(employees))
    await bot.send_message(message.chat.id, "\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                           reply_markup=types.ReplyKeyboardRemove())


async def generate_award_list_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    awards = session.query(Award).all()

    await call.message.answer(generate_award_list(awards))
    await call.message.answer("\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def generate_award_list_message_handler(message: types.Message, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    awards = session.query(Award).all()

    await bot.send_message(message.chat.id, generate_award_list(awards))
    await bot.send_message(message.chat.id, "\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                           reply_markup=types.ReplyKeyboardRemove())


async def generate_contract_list_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    contracts = session.query(Contract).all()

    await call.message.answer(generate_contract_list(contracts))
    await call.message.answer("\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def generate_contract_list_message_handler(message: types.Message, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    contracts = session.query(Contract).all()

    await bot.send_message(message.chat.id, generate_contract_list(contracts))
    await bot.send_message(message.chat.id, "\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                           reply_markup=types.ReplyKeyboardRemove())


def register_handlers_generate(dp: Dispatcher):
    dp.register_callback_query_handler(generate_list_vacancy_handler, lambda call: call.data == "gen_vacancy",
                                       state="*")
    dp.register_callback_query_handler(generate_list_vacancy_doc_handler, lambda call: call.data == "gen_doc_vac",
                                       state="*")

    dp.register_callback_query_handler(generate_list_profits_handler, lambda call: call.data == "gen_profit",
                                       state="*")
    dp.register_callback_query_handler(generate_doc_list_profits_handler, lambda call: call.data == "gen_doc_list_profits",
                                       state="*")
    # dp.register_message_handler(output_list_profits_handler, state=GenerateProfit.name_employee)

    dp.register_callback_query_handler(generate_list_warning_handler, lambda call: call.data == "gen_warning",
                                       state="*")
    dp.register_callback_query_handler(generate_doc_warning_list_handler, lambda call: call.data == "gen_doc_warnings",
                                       state="*")

    dp.register_callback_query_handler(generate_employee_list_handler, lambda call: call.data == "gen_employee_list",
                                       state="*")
    dp.register_message_handler(generate_employee_list_message_handler, commands=['employees'],
                                       state="*")

    dp.register_callback_query_handler(generate_award_list_handler, lambda call: call.data == "gen_award_list",
                                       state="*")
    dp.register_message_handler(generate_award_list_message_handler, commands=['awards'],
                                       state="*")

    dp.register_callback_query_handler(generate_contract_list_handler, lambda call: call.data == "gen_contract_list",
                                       state="*")
    dp.register_message_handler(generate_contract_list_message_handler, commands=['contracts'],
                                       state="*")

    dp.register_callback_query_handler(generate_list_employee_profit_handler,
                                       lambda call: call.data == "gen_employee_profit", state="*")
    dp.register_message_handler(output_list_employee_profit_handler, state=GenerateEmployeeProfit.name_employee)
