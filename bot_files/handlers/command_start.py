from aiogram import types, Dispatcher


from .utils import start_mesaage, start_message_users, start_message_admins, message_chat
from loging.main_log import entry_log
from bd_work.bd_regist import Search_date_DB, Add_Data_DB
from bot_files.state import Users, Admins


async def Cmd_Start(message: types.Message):
    if await Search_date_DB('admins', 'user_id', message.from_user.id):
        await message.answer(start_message_admins)
        await Admins.admin.set()
        await entry_log(message.from_user.full_name, "Отправил команду start и вошел"
                                                     " как администратор\n")
    elif await Search_date_DB('users', 'user_id', message.from_user.id):
        await message.answer(start_message_users)
        await Users.user.set()
        await entry_log(message.from_user.full_name, "Отправил команду start и вошел"
                                                     " как пользователь\n")
    else:
        await message.answer(start_mesaage, parse_mode='html')
        await Add_Data_DB('requests', user_id=message.from_user.id, profile_name=message.from_user.full_name)
        await entry_log(message.from_user.full_name, "Отправил команду start не имея доступ"
                                                     " к боту\n"
                                                     f"{message.from_user.full_name}"
                                                     " Был добавлен в таблицу запросов, если его в ней не было ранее\n")

# async def No_Cmd_Text(message: types.Message):
#     if await Search_date_DB('requests', 'user_id', message.from_user.id):
#         await message.answer(message_chat)
#     else:
#         await Add_Data_DB('requests', user_id=message.from_user.id, profile_name=message.from_user.full_name)
#         await message.answer(message_chat)
#     await entry_log(message.from_user.full_name, f"Отправил {message.text}, но этот пользователь еще не был"
#                                                  f" добавлен администратором\n")


def register_handler(dp: Dispatcher):
    dp.register_message_handler(Cmd_Start,
                                commands=['start'])
    # dp.register_message_handler(No_Cmd_Text)