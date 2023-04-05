from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bd_work.bd_regist import Get_Column, Add_Data_DB, Search_date_DB
from bot.state import Admins
from loging import entry_log

async def Cmd_Get_Requests(message: types.Message):
    requests_list = ''
    res = await Get_Column('requests', 'user_id', 'profile_name')
    for key, value in res.items():
        requests_list += f'{value}: {key}\n'
    await message.answer(f'Список запросов:\n<b>{requests_list}</b>',
                         parse_mode='html')
    await entry_log(message.from_user.full_name, "ввел команду GetRequests - администратор\n")

def register_handler(dp: Dispatcher):
    dp.register_message_handler(Cmd_Get_Requests,
                                commands=['GetRequests'],
                                state=Admins.admin)


async def Cmd_Add_User(message: types.Message):
    await message.answer("Введите никнейм пользователя, которому вы хотите предоставить пользовательский доступ.")
    await Admins.admin_add_user.set()
    await entry_log(message.from_user.full_name, "ввел команду AddUser - администратор\n")

async def Add_User(message: types.Message):
    if Search_date_DB('requests', profile_name=message.from_user.id):
        await Add_Data_DB('users', )