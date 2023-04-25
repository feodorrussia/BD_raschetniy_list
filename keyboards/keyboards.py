from aiogram import types

kb_hello = types.ReplyKeyboardMarkup(resize_keyboard=True)
but1 = types.KeyboardButton("Привет!")
kb_hello.add(but1)

kb_admin_def = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons = [types.InlineKeyboardButton(text="Добавление/назначение", callback_data="add_default"),
           types.InlineKeyboardButton(text="Изменение", callback_data="upd_default"),
           types.InlineKeyboardButton(text="Увольнение/удаление", callback_data="del_default"),
           types.InlineKeyboardButton(text="Генерация", callback_data="gen_default")]
kb_admin_def.add(*buttons)

