import copy
import os
import aiogram

import telebot
from telebot import types

from sqlalchemy.orm import sessionmaker
import datetime
from DataBase_setup import *

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

bot = telebot.TeleBot("6218189424:AAF4Upm5NsSzYh37T-UCUggbuGwSO5evPG8")  # SET TOKEN!!!!


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Привет!")
    markup.add(but1)

    bot.reply_to(message, f"Здравствуй, {message.from_user.first_name}\n(Будь паинькой, скажи привет)",
                 parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    if message.text.lower()[:5] == 'привет':
        bot.send_message(chat_id, "Если ты админ, скажи Да")
    if hash(message.text.lower()) == hash("да"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.InlineKeyboardButton(text="Добавление/назначение", callback_data="add_default"),
                   types.InlineKeyboardButton(text="Изменение", callback_data="upd_default"),
                   types.InlineKeyboardButton(text="Увольнение/удаление", callback_data="del_default"),
                   types.InlineKeyboardButton(text="Генерация", callback_data="gen_default")]
        markup.add(buttons)

        bot.send_message(chat_id, "Барин, добро пожаловать!\nЧего изволите?", reply_markup=markup)


@bot.callback_query_handler(text="add_default")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself, bitch")
    await call.answer()


@bot.callback_query_handler(text="upd_default")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself, bitch")
    await call.answer()


@bot.callback_query_handler(text="del_default")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself, bitch")
    await call.answer()


@bot.callback_query_handler(text="gen_default")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Go & fuck yourself")
    await call.answer()


bot.polling(none_stop=True)
