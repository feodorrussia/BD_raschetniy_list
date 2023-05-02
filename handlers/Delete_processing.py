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


async def name_employee_fire_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    await FireEmployee.next()
    await bot.send_message(chat_id,
                           "Введите дату увольнения сотрудника\n(если сотрудник уволен сегодня, то введите сегодняшнюю дату)",
                           reply_markup=types.ReplyKeyboardRemove())


async def date_fire_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

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


async def delete_contract_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteContract.name.set()
    await call.message.answer("Введите название контракта, который хотите закончить",
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_contract_delete_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    butts = [types.InlineKeyboardButton(text="Да", callback_data="delete_contract"),
             types.InlineKeyboardButton(text="Нет", callback_data="cancel_deleting_contract")]
    kb_continue.add(*butts)

    await DeleteContract.next()

    await bot.send_message(chat_id,
                           "Контракт найден. Уверены, что хотите удалить все записи, связанные с этим контрактом?\nВосстановление данных будет далее невозвожно.",
                           reply_markup=kb_continue)


async def cancel_contract_deleting_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_contract")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Хорошо, удаление отменено." +
                           "\nКонтракт удалён.\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def contract_delete_check_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_contract")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Все связанные с контрактом данные из таблиц Ставки, Должности и удалены." +
                           "\nКонтракт удалён.\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def delete_child_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeleteChild.name_employee.set()

    await call.message.answer("Введите ФИО сотрудника", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_employee_child_delete_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    children = [[1, "2022.03.02"], [2, "2022.01.02"], [3, "2022.05.22"]]

    kb_children = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    butts = [types.InlineKeyboardButton(text=child[1], callback_data=f"delete_child_{child[0]}") for child in children]
    kb_children.add(*butts)

    await DeleteChild.next()

    await bot.send_message(chat_id,
                           "Сотрудник найден. Выберите дату рождения ребёнка, которую хотите удалить",
                           reply_markup=kb_children)


async def child_delete_date_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    id_child = int(call.data.split("_")[-1])
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_child")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, f"Дата рождения ребёнка {id_child} удалена." +
                           "\nКонтракт удалён.\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def delete_award_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    kb_award = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butts = [types.KeyboardButton("Поощрение"), types.KeyboardButton("Штраф")]
    kb_award.add(*butts)

    await DeleteAward.type.set()
    await call.message.answer("Введите тип (поощрение/штраф)", reply_markup=kb_award)
    await call.answer()


async def type_delete_award_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    await DeleteAward.next()

    await bot.send_message(chat_id, f"Введите название {'поощрением/штрафом'}, которое хотите удалить",
                           reply_markup=types.ReplyKeyboardRemove())


async def name_award_delete_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    butts = [types.InlineKeyboardButton(text="Да", callback_data="delete_award"),
             types.InlineKeyboardButton(text="Нет", callback_data="cancel_deleting_award")]
    kb_continue.add(*butts)

    await DeleteAward.next()

    await bot.send_message(chat_id,
                           f"{'Поощрение/Штраф найден'}. Уверены, что хотите удалить все записи, связанные с этим {'поощрением/штрафом'}?\nВосстановление данных будет далее невозвожно.",
                           reply_markup=kb_continue)


async def cancel_award_deleting_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_award")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Хорошо, удаление отменено." +
                           "\nКонтракт удалён.\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def award_delete_check_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_award")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id,
                           f"Все связанные с {'поощрением/штрафом'} данные из таблиц Ставки, Должности и удалены." +
                           "\nКонтракт удалён.\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def delete_position_handler(call: types.CallbackQuery, state: FSMContext):
    # await remove_chat_buttons(chat_id)
    await DeletePosition.name.set()
    await call.message.answer("Введите название должности", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()


async def name_position_delete_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    butts = [types.InlineKeyboardButton(text="Да", callback_data="delete_position"),
             types.InlineKeyboardButton(text="Нет", callback_data="cancel_deleting_position")]
    kb_continue.add(*butts)

    await DeletePosition.next()

    await bot.send_message(chat_id, "Должность найдена. Уверены, что хотите удалить все записи, связанные с этой должностью?\nВосстановление данных будет далее невозвожно", reply_markup=kb_continue)


async def cancel_position_deleting_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_position")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Хорошо, удаление отменено." +
                           "\nКонтракт удалён.\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


async def position_delete_check_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    # await remove_chat_buttons(chat_id)

    kb_continue = types.InlineKeyboardMarkup(resize_keyboard=True)
    butts = types.InlineKeyboardButton(text="Продолжить", callback_data="del_position")
    kb_continue.add(butts)

    await state.finish()
    await AdminStatus.authorized.set()

    await bot.send_message(chat_id, "Все связанные с контрактом данные из таблиц Ставки, Должности и удалены." +
                           "\nКонтракт удалён.\n\nМеню - /start_menu" +
                           "\nМеню добавления - /add_menu" +
                           "\nМеню удаления - /del_menu" +
                           "\nМеню изменения - /upd_menu" +
                           "\nМеню запросов - /gen_menu\n\nВыйти - /exit", reply_markup=kb_continue)


def register_handlers_delete(dp: Dispatcher):
    dp.register_callback_query_handler(fire_employee_handler, lambda call: call.data == "del_employee",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_employee_fire_handler, state=FireEmployee.name_employee)
    dp.register_message_handler(date_fire_handler, state=FireEmployee.date_fire)

    dp.register_callback_query_handler(delete_contract_handler, lambda call: call.data == "del_contract",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_contract_delete_handler, state=DeleteContract.name)
    dp.register_callback_query_handler(contract_delete_check_handler, lambda call: call.data == "delete_contract",
                                       state=DeleteContract.check)
    dp.register_callback_query_handler(cancel_contract_deleting_handler,
                                       lambda call: call.data == "cancel_deleting_contract",
                                       state=DeleteContract.check)

    dp.register_callback_query_handler(delete_child_handler, lambda call: call.data == "del_child",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_employee_child_delete_handler, state=DeleteChild.name_employee)
    dp.register_callback_query_handler(child_delete_date_handler, state=DeleteChild.date)

    dp.register_callback_query_handler(delete_award_handler, lambda call: call.data == "del_award",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(type_delete_award_handler, state=DeleteAward.type)
    dp.register_message_handler(name_award_delete_handler, state=DeleteAward.name)
    dp.register_callback_query_handler(award_delete_check_handler, lambda call: call.data == "delete_award",
                                       state=DeleteAward.check)
    dp.register_callback_query_handler(cancel_award_deleting_handler,
                                       lambda call: call.data == "cancel_deleting_award",
                                       state=DeleteAward.check)

    dp.register_callback_query_handler(delete_position_handler, lambda call: call.data == "del_position",
                                       state=AdminStatus.authorized)
    dp.register_message_handler(name_position_delete_handler, state=DeletePosition.name)
    dp.register_callback_query_handler(position_delete_check_handler, lambda call: call.data == "delete_position",
                                       state=DeletePosition.check)
    dp.register_callback_query_handler(cancel_position_deleting_handler,
                                       lambda call: call.data == "cancel_deleting_position",
                                       state=DeletePosition.check)
