from aiogram.utils import executor

from bot_files.create_bot import dp
from bot_files.handlers import command_start
from bot_files.admin import admin_commands
from bot_files.user import user_commands


async def on_startup(_):
    print('Бот запустился!')

def start_bot():

    command_start.register_handler(dp)
    admin_commands.register_handler(dp)
    user_commands.register_handler(dp)

    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)