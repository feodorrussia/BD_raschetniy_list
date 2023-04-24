from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import *


# @dp.message_handler()
async def echo_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, message.text, reply_markup=kb_admin_def)

# @bot.callback_query_handler(text="add_default")
async def add_default(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself, bitch")
    await call.answer()


# @bot.callback_query_handler(text="upd_default")
async def upd_default(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself, bitch")
    await call.answer()


# @bot.callback_query_handler(text="del_default")
async def del_default(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself, bitch")
    await call.answer()


# @bot.callback_query_handler(text="gen_default")
async def gen_default(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself")
    await call.answer()

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(echo_message)
    dp.register_callback_query_handler(add_default)
    dp.register_callback_query_handler(upd_default)
    dp.register_callback_query_handler(del_default)
    dp.register_callback_query_handler(gen_default)
