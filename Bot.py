import copy
import os
import shutil

import telebot
from telebot import types

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from DataBase_setup import *

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

bot = telebot.TeleBot("")  # SET!!!!


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Добавление файлов")
    but2 = types.KeyboardButton("Таблица распределения")
    but3 = types.KeyboardButton("Статистика для человека")
    but4 = types.KeyboardButton("Закончить")
    markup.add(but1, but2, but3, but4)

    bot.reply_to(message, f"Здравствуй, {message.from_user.first_name}\nВыбери, что делать дальше",
                 parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        global path
        src = path + "Inputs/" + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(func=lambda message: True)
def handle_docs(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Добавление файлов")
    but2 = types.KeyboardButton("Таблица распределения")
    but3 = types.KeyboardButton("Статистика для человека")
    but4 = types.KeyboardButton("Закончить")
    markup.add(but1, but2, but3, but4)

    global flag_stat

    if message.chat.type == 'private':
        if message.text == "Добавление файлов":
            bot.send_message(message.chat.id, "Хорошо, ловлю\n" +
                             "Обязательные названия файлов:\n" +
                             "Form.xls - таблица с данными из гугл-формы\n" +
                             "Koef.xls - таблица матрицой коэффициентов пар\n" +
                             "Profiles.xls - таблица направлениями и количеством групп", reply_markup=markup)

        elif message.text == "Таблица распределения":
            chat_id = message.chat.id
            # bot.send_document(chat_id, doc)

        elif message.text == "Статистика для человека":
            chat_id = message.chat.id
            flag_stat = True
            bot.send_message(chat_id, "Введите ФИ человека")

        elif flag_stat:
            name = message.text

            chat_id = message.chat.id
            # bot.send_message(chat_id, person_Stat(id_p))
            flag_stat = False

        elif message.text == "Закончить":
            shutil.rmtree(path + "Inputs")
            shutil.rmtree(path + "Outputs")

            os.mkdir(path + "Inputs")
            os.mkdir(path + "Outputs")
            bot.send_message(message.chat.id, "Хорошо, все файлы удалены\nДо новых встреч")

        else:
            bot.send_message(message.chat.id, "Я не знаю что и ответить")


bot.polling(none_stop=True)
