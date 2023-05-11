from aiogram import Dispatcher
from create_bot import bot
from keyboards.keyboards import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.AdminStatus import AdminStatus


# @dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await AdminStatus.unauthorized.set()
    await message.reply(f"Здравствуй, {message.from_user.first_name}\n\nАвторизоваться - /admin")


# @dp.message_handler()
async def echo(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, message.text)



async def authorizing_handler(message: types.Message, state : FSMContext):
    chat_id = message.chat.id
    await AdminStatus.authorizing.set()
    await bot.send_message(chat_id, "Введи пароль")


async def authorization_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    print(hash("пароль"))
    if hash(message.text) == hash("да"):
        await AdminStatus.authorized.set()
        await bot.send_message(chat_id, "Здравствуйте, Барин. Чего изволите?", reply_markup=kb_admin_def)
    else:
        await bot.send_message(chat_id, "Неверный ответ, сударь. Изволь ещё раз.")



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(authorizing_handler, state=AdminStatus.unauthorized, commands=['admin'])
    dp.register_message_handler(authorizing_handler, Text(equals="войти", ignore_case=True), state=AdminStatus.unauthorized)
    dp.register_message_handler(authorization_handler, state=AdminStatus.authorizing)
    dp.register_message_handler(echo, state=AdminStatus.unauthorized)
