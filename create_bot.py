import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from sqlalchemy.orm import sessionmaker
from data.DataBase_setup import *

engine = create_engine('sqlite:///data/database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6218189424:AAF4Upm5NsSzYh37T-UCUggbuGwSO5evPG8")  #
dp = Dispatcher(bot, storage=storage)

data_name_file = "data_file.json"