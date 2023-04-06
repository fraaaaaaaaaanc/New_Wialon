from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bd_work.bd_regist import Get_Column, Add_Data_DB, Search_date_DB, Get_Data, Delete_Data
from bot.state import Admins
from loging import entry_log

async def Cmd_Get_Requests(message: types.Message):
    requests_list = ''
    result_list_id = await Get_Column('requests', 'user_id')
    result_list_name = await Get_Column('requests', 'profile_name')
    for name, id in zip(result_list_name, result_list_id):
        requests_list += f'{name}: {id}\n'
    await message.answer(f'Список запросов:\n<b>{requests_list}</b>',
                         parse_mode='html')
    await entry_log(message.from_user.full_name, "ввел команду GetRequests - администратор\n")


async def Cmd_Add_User(message: types.Message):
    await message.answer("Введите никнейм пользователя, которому вы хотите предоставить пользовательский доступ.")
    await Admins.admin_add_user.set()
    await entry_log(message.from_user.full_name, "ввел команду AddUser - администратор\n")

async def Add_User(message: types.Message):
    if await Search_date_DB('requests', 'profile_name', message.text):
        user_id = await Get_Data('requests', 'user_id', 'profile_name', message.text)
        await Add_Data_DB('users', user_id=user_id, profile_name=str(message.text))
        await Delete_Data('requests', 'profile_name', message.text)
        await message.answer(f"Пользователю {message.text}, открыт пользовательский доступ!")
        await message.bot.send_message(user_id, "Администратор открыл для вас пользовательский доступ в боте!")
        await entry_log(message.from_user.full_name, f"открыл пользовательский доступ для "
                                                     f"{message.text}\n Пользователю {message.text} было"
                                                     f" отправлено сообщение- администратор\n")
        await Admins.admin.set()
    else:
        await message.answer("Пользователь с такими никнеймом не отправлял запрос в данном боте, попробуйте отправить"
                             " никнейм еще раз.")

def register_handler(dp: Dispatcher):
    dp.register_message_handler(Cmd_Get_Requests,
                                commands=['GetRequests'],
                                state=Admins.admin)
    dp.register_message_handler(Cmd_Add_User,
                                commands=['AddUser'],
                                state=Admins.admin)
    dp.register_message_handler(Add_User,
                                state=Admins.admin_add_user)
