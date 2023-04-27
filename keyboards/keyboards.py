from aiogram import types
from create_bot import bot

kb_hello = types.ReplyKeyboardMarkup(resize_keyboard=True)
but_hello = types.KeyboardButton("Привет!")
kb_hello.add(but_hello)

kb_admin_def = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
buttons = [types.InlineKeyboardButton(text="Добавление/назначение", callback_data="add_default"),
           types.InlineKeyboardButton(text="Изменение", callback_data="upd_default"),
           types.InlineKeyboardButton(text="Увольнение/удаление", callback_data="del_default"),
           types.InlineKeyboardButton(text="Генерация", callback_data="gen_default")]
kb_admin_def.add(*buttons)

kb_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
but_cancel = types.KeyboardButton("Отмена")
kb_cancel.add(but_cancel)


async def remove_chat_buttons(chat_id: int):
    msg = await bot.send_message(chat_id, "",
                                 reply_markup=types.ReplyKeyboardRemove(),
                                 parse_mode="MarkdownV2")
    await msg.delete()

