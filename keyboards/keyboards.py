from aiogram import types
from create_bot import bot

kb_hello = types.ReplyKeyboardMarkup(resize_keyboard=True)
but_hello = types.KeyboardButton("Привет!")
kb_hello.add(but_hello)

kb_admin_def = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons_1 = [types.InlineKeyboardButton(text="Добавление/назначение", callback_data="add_default"),
           types.InlineKeyboardButton(text="Изменение", callback_data="upd_default"),
           types.InlineKeyboardButton(text="Увольнение", callback_data="del_default"),
           types.InlineKeyboardButton(text="Генерация", callback_data="gen_default")]
kb_admin_def.add(*buttons_1)

kb_add_def = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons_2 = [types.InlineKeyboardButton(text="Сотрудник", callback_data="add_employee"),
           types.InlineKeyboardButton(text="Ребёнок сотрудника", callback_data="add_child"),
           types.InlineKeyboardButton(text="Контракт", callback_data="add_contract"),
           types.InlineKeyboardButton(text="Новая должность", callback_data="add_position"),
           types.InlineKeyboardButton(text="Контракт сотруднику", callback_data="add_contract_to_employee"),
           types.InlineKeyboardButton(text="Новое поощрение/штраф", callback_data="add_award"),
           types.InlineKeyboardButton(text="Поощрение/штраф сотруднику", callback_data="add_award_to_employee")]
kb_add_def.add(*buttons_2)

kb_del_def = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons_3 = [types.InlineKeyboardButton(text="Сотрудник", callback_data="del_employee")]
kb_del_def.add(*buttons_3)
""",
            types.InlineKeyboardButton(text="Контракт", callback_data="del_contract"),
            types.InlineKeyboardButton(text="Ребёнок", callback_data="del_child"),
            types.InlineKeyboardButton(text="Поощрение/штраф", callback_data="del_award"),
            types.InlineKeyboardButton(text="Должность", callback_data="del_position")"""

kb_gen_def = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons_4 = [types.InlineKeyboardButton(text="Список вакансий", callback_data="gen_vacancy"),
            types.InlineKeyboardButton(text="Расчётный лист сотрудника", callback_data="gen_employee_profit"),
            types.InlineKeyboardButton(text="Предупреждения", callback_data="gen_warning"),
            types.InlineKeyboardButton(text="Предупреждения", callback_data="gen_employee_list"),
            types.InlineKeyboardButton(text="Предупреждения", callback_data="gen_award_list"),
            types.InlineKeyboardButton(text="Предупреждения", callback_data="gen_contract_list"),
            types.InlineKeyboardButton(text="Годовой доход всех сотрудников", callback_data="gen_profit")]
kb_gen_def.add(*buttons_4)

kb_edit_def = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons_5 = [types.InlineKeyboardButton(text="Ставка сотрудника", callback_data="edit_rate")]
kb_edit_def.add(*buttons_5)
"""types.InlineKeyboardButton(text="Сотрудник", callback_data="edit_employee"),
            types.InlineKeyboardButton(text="Ребёнок", callback_data="edit_child"),,
            types.InlineKeyboardButton(text="Контракт", callback_data="edit_contract"),
            types.InlineKeyboardButton(text="Должность", callback_data="edit_position"),
            types.InlineKeyboardButton(text="Поощрение/штраф", callback_data="edit_award"),
            types.InlineKeyboardButton(text="Поощрения/штрафы сотрудника", callback_data="edit_award_employee")
            """

kb_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
but_cancel = types.KeyboardButton("Отмена")
kb_cancel.add(but_cancel)


async def remove_chat_buttons(chat_id: int):
    msg = await bot.send_message(chat_id, "",
                                 reply_markup=types.ReplyKeyboardRemove(),
                                 parse_mode="MarkdownV2")
    await msg.delete()

