from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

async def Main_User_Menu():
    menu_user = ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
        [KeyboardButton('/EmptyReport'), KeyboardButton('/FillReport')],
    ])

    return menu_user