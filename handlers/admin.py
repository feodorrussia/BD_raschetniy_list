from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards.keyboards import kb_cancel, kb_admin_def, kb_add_def, kb_del_def, kb_gen_def, kb_edit_def
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.AdminStatus import AdminStatus


# @dp.message_handler()
async def menu_handler(message: types.Message, state : FSMContext):
    chat_id = message.chat.id
    # await remove_chat_buttons(chat_id)
    await bot.send_message(chat_id, "Чего изволите?\nВыйти - /exit", reply_markup=kb_admin_def)

# @dp.callback_query_handler(Text("add_default"))
async def add_default_handler(call: types.CallbackQuery):
    await call.message.answer("Выберите, что/кого Вы хотите добавить\nМеню - /start_menu", reply_markup=kb_add_def)
    await call.answer()

async def add_menu_handler(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Выберите, что/кого Вы хотите добавить\nМеню - /start_menu", reply_markup=kb_add_def)


# @bot.callback_query_handler(text="upd_default")
async def edit_default_handler(call: types.CallbackQuery):
    await call.message.answer("Выберите, что/кого Вы хотите изменить\nМеню - /start_menu", reply_markup=kb_edit_def)
    await call.answer()

async def edit_menu_handler(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Выберите, что/кого Вы хотите изменить\nМеню - /start_menu", reply_markup=kb_edit_def)


# @bot.callback_query_handler(text="del_default")
async def del_default_handler(call: types.CallbackQuery):
    await call.message.answer("Выберите, что/кого Вы хотите удалить/уволить/завершить\nМеню - /start_menu", reply_markup=kb_del_def)
    await call.answer()

async def del_menu_handler(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Выберите, что/кого Вы хотите удалить/уволить/завершить\nМеню - /start_menu", reply_markup=kb_del_def)


# @bot.callback_query_handler(text="gen_default")
async def gen_default_handler(call: types.CallbackQuery):
    await call.message.answer("Выберите, что Вы хотите сгенерировать\nМеню - /start_menu", reply_markup=kb_gen_def)
    await call.answer()

async def gen_menu_handler(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Выберите, что Вы хотите сгенерировать\nМеню - /start_menu", reply_markup=kb_gen_def)


async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return
    if current_state == "AdminStatus:authorizing":
        await AdminStatus.unauthorized.set()
        await message.reply("Как скажете, Барин.\nАвторизоваться снова - /admin", reply_markup=types.ReplyKeyboardRemove())
        return

    await AdminStatus.authorized.set()
    await message.reply("Как скажете, Барин.\nМеню - /start_menu\nВыйти - /exit", reply_markup=types.ReplyKeyboardRemove())


async def exit_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await AdminStatus.unauthorized.set()
    await message.reply("Как скажете, Барин.\nАвторизоваться - /admin", reply_markup=types.ReplyKeyboardRemove())

async def help_handler(message : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await AdminStatus.authorized.set()
    await message.reply("Всегда рад, Барин.\nВы в любой момент можете написать <b>отмена</b> или ввести команду /cancel - текущая задача остановится и Вы перейдёте в начало."+
                        "\nМеню - /start_menu\nПомощь - /help\nВыйти - /exit",
                           parse_mode="html", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(menu_handler, commands=['start_menu'], state=AdminStatus.authorized)
    dp.register_message_handler(menu_handler, Text(equals="меню", ignore_case=True), state=AdminStatus.authorized)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(help_handler, state="*", commands=['help'])
    dp.register_message_handler(help_handler, Text(equals="помоги", ignore_case=True), state="*")
    dp.register_message_handler(exit_handler, state=AdminStatus.authorized, commands=['exit'])
    dp.register_message_handler(exit_handler, Text(equals="выйти", ignore_case=True), state=AdminStatus.authorized)


    dp.register_message_handler(add_menu_handler, commands=['add_menu'], state=AdminStatus.authorized)
    dp.register_callback_query_handler(add_default_handler, lambda call: call.data == "add_default", state=AdminStatus.authorized)

    dp.register_message_handler(edit_menu_handler, commands=['upd_menu'], state=AdminStatus.authorized)
    dp.register_callback_query_handler(edit_default_handler, lambda call: call.data == "upd_default", state=AdminStatus.authorized)

    dp.register_message_handler(del_menu_handler, commands=['del_menu'], state=AdminStatus.authorized)
    dp.register_callback_query_handler(del_default_handler, lambda call: call.data == "del_default", state=AdminStatus.authorized)

    dp.register_message_handler(gen_menu_handler, commands=['gen_menu'], state=AdminStatus.authorized)
    dp.register_callback_query_handler(gen_default_handler, lambda call: call.data == "gen_default", state=AdminStatus.authorized)
