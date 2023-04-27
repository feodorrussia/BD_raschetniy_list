from create_bot import *
from handlers.client import *
from handlers.admin import *
from handlers.Add_proccessing import *
from handlers.Delete_proccessing import *
from handlers.Generation_proccessing import *
from handlers.Update_proccessing import *


register_handlers_client(dp)
register_handlers_admin(dp)
register_handlers_add(dp)

if __name__ == '__main__':
    executor.start_polling(dp)
