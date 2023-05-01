from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import kb_cancel
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.GeneratingStates import *
from states.AdminStatus import AdminStatus


async def generate_list_vacancy_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    list_vacancies = ["Программист - 2 x 10 000", "Инженер - 3 x 10 000"]

    kb_doc = types.InlineKeyboardMarkup(resize_keyboard=True)
    butt = types.InlineKeyboardButton(text="Файл", callback_data="gen_doc_vac")
    kb_doc.add(butt)

    await call.message.answer("Ваш список вакансий. Хотите получить список файлом?\n\n" +
                              "№ - Название - N полных ставок Х Зарплата:\n{}\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit".format(
                                  "\n".join([str(i) + ". " + list_vacancies[i] for i in range(len(list_vacancies))])),
                              reply_markup=kb_doc)
    await call.answer()


async def generate_list_vacancy_doc_handler(call: types.CallbackQuery, message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    list_vacancies = ["Программист - 2 x 10 000", "Инженер - 3 x 10 000"]

    with open(f"data/vacancy_{hash(chat_id)}.txt", "w") as file:
        file.write("Список вакансий:\n" +
                   "№ - Название - N полных ставок Х Зарплата:\n" +
                   "\n".join([str(i) + ". " + list_vacancies[i] for i in range(len(list_vacancies))]))
        file.close()

    await call.message.answer("Ваш файл:\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())

    with open(f"data/vacancy_{hash(chat_id)}.txt", "r") as file:
        await bot.send_file(chat_id, file)
        file.close()

    await call.answer()


async def generate_list_profits_handler(call: types.CallbackQuery, message: types.Message, state: FSMContext):
    # await remove_chat_buttons(chat_id)

    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    list_vacancies = ["Соломатов Александр Денисович - -1000", "Ушкарёв Савва - -100 000"]

    with open(f"data/profits_{hash(chat_id)}.txt", "w") as file:
        file.write("Итоговый расчётный лист сотрудников:\n" +
                   "№ - ФИО сотрудника - Итоговый расчёт за полседний месяц:\n" +
                   "\n".join([str(i) + ". " + list_vacancies[i] for i in range(len(list_vacancies))]))
        file.close()

    await call.message.answer("Ваш расчётный лист:\n\nМеню - /start_menu" +
                              "\nМеню добавления - /add_menu" +
                              "\nМеню удаления - /del_menu" +
                              "\nМеню изменения - /upd_menu" +
                              "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())

    with open(f"data/profits_{hash(chat_id)}.txt", "r") as file:
        await bot.send_file(chat_id, file)
        file.close()

    await call.answer()


async def generate_list_warning_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    # await GenerateWarning.name_employee.set()

    list_employees = ["Соломатов Александр Денисович", "Ушкарёв Савва"]

    await call.message.answer(
        "Итоговый расчёт за месяц меньше нуля у следующих сотрудников:\n\n".format(
            "\n".join([str(i) + ". " + list_employees[i] for i in range(len(list_employees))])),
        reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def generate_list_employee_profit_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await GenerateEmployeeProfit.name_employee.set()

    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def output_list_employee_profit_handler(message: types.Message):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    list_pays = [["Соломатов Александр Денисович", -1000], ["Щтраф", "Опоздание", -1000], ["Поощрение", "Жив", 0]]

    # with open(f"data/profit_{list_pays[0][0]}_{hash(chat_id)}.txt", "w") as file:  # hash(
    #     text = f"Расчётный лист\nФИО: {list_pays[0][0]}\n\n№ - Название начисления - Итоговый расчёт за полседний месяц:\n"
    #     text += "\n".join(
    #         [str(i) + ". " + " - ".join(list(map(lambda x: str(x), list_pays[i]))) for i in range(1, len(list_pays))])
    #     text += f"\nИтого: {list_pays[0][1]}"
    #     file.write(text)
    #     file.close()

    text = f"Расчётный лист\nФИО: {list_pays[0][0]}\n\n№ - Название начисления - Итоговый расчёт за полседний месяц:\n"
    text += "\n".join(
        [str(i) + ". " + " - ".join(list(map(lambda x: str(x), list_pays[i]))) for i in range(1, len(list_pays))])
    text += f"\nИтого: {list_pays[0][1]}"

    await bot.send_message(chat_id, f"Расчётный лист для сотрудника ФИО: {list_pays[0][0]}\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())

    await bot.send_message(chat_id, text, reply_markup=types.ReplyKeyboardRemove())

    # with open(f"data/profit_{list_pays[0][0]}_{hash(chat_id)}.txt", "r") as file:  # hash(
    #     await bot.send_file(chat_id, file)
    #     file.close()


def register_handlers_generate(dp: Dispatcher):
    dp.register_callback_query_handler(generate_list_vacancy_handler, lambda call: call.data == "gen_vacancy",
                                       state=AdminStatus.authorized)
    dp.register_callback_query_handler(generate_list_vacancy_doc_handler, lambda call: call.data == "gen_doc_vac",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(generate_list_profits_handler, lambda call: call.data == "gen_profit",
                                       state=AdminStatus.authorized)
    # dp.register_message_handler(output_list_profits_handler, state=GenerateProfit.name_employee)

    dp.register_callback_query_handler(generate_list_warning_handler, lambda call: call.data == "gen_warning",
                                       state=AdminStatus.authorized)

    dp.register_callback_query_handler(generate_list_employee_profit_handler,
                                       lambda call: call.data == "gen_employee_profit", state=AdminStatus.authorized)
    dp.register_message_handler(output_list_employee_profit_handler, state=GenerateEmployeeProfit.name_employee)