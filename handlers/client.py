from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import *


# @dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f"Здравствуй, {message.from_user.first_name}\n(Будь паинькой, скажи привет)",
                       reply_markup=kb_hello)


# @dp.message_handler(commands=['Admin'])
async def process_authorize_command(message: types.Message):
    chat_id = message.chat.id

    await bot.send_message(chat_id, "Если ты админ, скажи Да")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_authorize_command, commands=['Admin'])
