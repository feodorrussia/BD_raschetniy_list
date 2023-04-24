from create_bot import *
from handlers.client import *
from handlers.admin import *


register_handlers_client(dp)
register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp)
