from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.keyboards import *


# @dp.message_handler()
async def echo_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, message.text)

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(echo_message)