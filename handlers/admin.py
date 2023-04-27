from aiogram import Dispatcher
from create_bot import bot
from keyboards.keyboards import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.AdminStatus import AdminStatus


# @dp.message_handler()
async def menu_handler(message: types.Message, state : FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    await bot.send_message(chat_id, "What do you want?", reply_markup=kb_admin_def)

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


async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    if current_state == "AdminStatus:authorizing":
        await AdminStatus.unauthorized.set()
        await message.reply("No problem, bro")
        return
    await AdminStatus.authorized.set()
    await message.reply("No problem, bro")


async def exit_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await AdminStatus.unauthorized.set()
    await message.reply("No problem, bro. U r free now")

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(menu_handler, commands=['start_menu'], state=AdminStatus.authorized)
    dp.register_message_handler(menu_handler, Text(equals="меню", ignore_case=True), state=AdminStatus.authorized)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(exit_handler, state="*", commands='exit')
    dp.register_message_handler(exit_handler, Text(equals="выйти", ignore_case=True), state="*")

    dp.register_callback_query_handler(add_default)
    dp.register_callback_query_handler(upd_default)
    dp.register_callback_query_handler(del_default)
    dp.register_callback_query_handler(gen_default)
