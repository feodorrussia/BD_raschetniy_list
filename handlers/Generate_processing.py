from aiogram import types, Dispatcher
from create_bot import *
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.GeneratingStates import *
from states.AdminStatus import AdminStatus
from other.functions import *


def list_vacancies_func():
    result = ["Программист - 2 x 10 000", "Инженер - 3 x 10 000"]
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
                result.append(f"{position.name} - {count*position.staff_num*100}% x {position.wage} р.")
    return result


async def generate_list_vacancy_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    list_vacancies = list_vacancies_func()

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_vac")
    kb_doc.add(butt)

    await call.message.answer("Ваш список вакансий. Хотите получить список файлом?\n\n" +
                              "№ - Название - N полных ставок Х Зарплата:\n{}\n\nМеню - /start_menu".format(
                                  "\n".join(
                                      [str(i + 1) + ". " + list_vacancies[i] for i in range(len(list_vacancies))])) +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit",
                              reply_markup=kb_doc)
    await call.answer()


async def generate_list_vacancy_doc_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    # await remove_chat_buttons(chat_id)
    list_vacancies = list_vacancies_func()

    with open(f"data/vacancy_{hash(chat_id)}.txt", "w") as file:
        file.write("Список вакансий:\n\n" +
                   "№ - Название - N полных ставок Х Зарплата:\n" +
                   "\n".join([str(i + 1) + ". " + list_vacancies[i] for i in range(len(list_vacancies))]))
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


def list_profits():
    list_vacancies = ["Соломатов Александр Денисович - -1000", "Ушкарёв Савва - -100 000"]

    text ="Итоговый расчётный лист сотрудников:\n\n" + "№ - ФИО сотрудника - Итоговый расчёт за последний месяц:\n"
    text += "\n".join([str(i + 1) + ". " + list_vacancies[i] for i in range(len(list_vacancies))])
    text += f"\nИтого: {-101000}"

    return text


async def generate_list_profits_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)

    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_list_profits")
    kb_doc.add(butt)

    await bot.send_message(call.message.chat.id, list_profits(), reply_markup=kb_doc)

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
        file.write(list_profits())
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
    list_employees = ["Соломатов Александр Денисович", "Ушкарёв Савва"]

    text = "Итоговый расчёт за месяц меньше нуля у следующих сотрудников:\n\n"
    text += "\n".join([str(i + 1) + ". " + list_employees[i] for i in range(len(list_employees))])

    text = "Не продлён основной контракт и сотрудник не уволен!\n\n"
    text += "\n".join([str(i + 1) + ". " + list_employees[i] for i in range(len(list_employees))])

    return text


async def generate_list_warning_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_list_profits")
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


def employee_profit_list(employee_id):
    list_pays = [["Соломатов Александр Денисович", -1000], ["Щтраф", "Опоздание", -1000], ["Поощрение", "Жив", 0]]

    text = f"Расчётный лист\nФИО: {list_pays[0][0]}\n"
    text += "\n---------------------\n\t Контракты\n\t Название, Тип - ставка х ЗП = оплата\n---------------------\n\n"
    text += "\n".join([str(i + 1) + ". " + " - ".join(list(map(lambda x: str(x), list_pays[i]))) for i in range(1, len(list_pays))])
    text += "\n\n---------------------\n\t Поощрения\n\t Название, Тип = счёт\n---------------------\n\n"
    text += "\n".join([str(i + 1) + ". " + " - ".join(list(map(lambda x: str(x), list_pays[i]))) for i in range(1, len(list_pays))])
    text += "\n\n---------------------\n\t Штрафы\n\t Название, Тип = счёт\n---------------------\n\n"
    text += "\n".join([str(i + 1) + ". " + " - ".join(list(map(lambda x: str(x), list_pays[i]))) for i in range(1, len(list_pays))])
    text += "\n\n---------------------\n\t Налоги и вычет\n---------------------\n\n"
    text += "\n".join([str(i + 1) + ". " + " - ".join(list(map(lambda x: str(x), list_pays[i]))) for i in range(1, len(list_pays))])
    text += f"\nИтого: {list_pays[0][1]}"

    return text


async def generate_list_employee_profit_handler(call: types.CallbackQuery):
    # await remove_chat_buttons(chat_id)
    await GenerateEmployeeProfit.name_employee.set()

    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def output_list_employee_profit_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_list_profits")
    kb_doc.add(butt)

    await bot.send_message(chat_id, employee_profit_list(1), reply_markup=kb_doc)

    await bot.send_message(chat_id, f"Меню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())


async def generate_doc_employee_profit_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)

    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    with open(f"data/employee_profit_{hash(chat_id)}.txt", "w") as file:
        file.write(employee_profit_list(1))
        file.close()

    with open(f"data/employee_profit_{hash(chat_id)}.txt", "rb") as file:
        await bot.send_document(chat_id, file)
        file.close()

    await call.message.answer("Ваш файл с расчётным листом\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())

    await call.answer()


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
    # dp.register_message_handler(output_list_profits_handler, state=GenerateProfit.name_employee)

    dp.register_callback_query_handler(generate_list_warning_handler, lambda call: call.data == "gen_warning",
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
