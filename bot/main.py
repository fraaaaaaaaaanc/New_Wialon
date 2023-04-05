from aiogram.utils import executor

from bot.create_bot import dp
from bot.handlers import command_start


async def on_startup(_):
    print('Бот запустился!')

def start_bot():

    command_start.register_handler(dp)
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)