from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def add_admin_inline_keyboard():
    add_admin_ikb = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[
        [InlineKeyboardButton('Запросов', callback_data='requests'),
         InlineKeyboardButton('Пользователей ', callback_data='users')],
    ])

    return add_admin_ikb