import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from other.config_reader import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import client, admin

from sqlalchemy.orm import sessionmaker
from data.DataBase_setup import *

engine = create_engine('sqlite:///data/database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())  # безопашношть
dp = Dispatcher(bot, storage=storage)

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


if __name__ == '__main__':
    executor.start_polling(dp)
