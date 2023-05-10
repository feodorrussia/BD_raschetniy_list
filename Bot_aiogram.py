from create_bot import dp, executor
from handlers.client import register_handlers_client
from handlers.admin import register_handlers_admin
from handlers.Add_processing import register_handlers_add
from handlers.Delete_processing import register_handlers_delete
from handlers.Generate_processing import register_handlers_generate
from handlers.Edit_processing import register_handlers_edit


register_handlers_client(dp)
register_handlers_admin(dp)
register_handlers_generate(dp)
register_handlers_add(dp)
register_handlers_delete(dp)
register_handlers_edit(dp)

if __name__ == '__main__':
    executor.start_polling(dp)
