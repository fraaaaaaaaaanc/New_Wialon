from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bd_work.bd_regist import Get_Column, Add_Data_DB, Search_date_DB, Get_Data, Delete_Data
from bot_files.state import Admins
from loging import entry_log
from bot_files.keyboards import Main_Admin_Menu, add_admin_inline_keyboard
from .utils import get_datas_table, Add_New_Record, Main_Admin_Menu_Text


async def Cmd_Get_Requests(message: types.Message):
    requests_list = await get_datas_table('requests')
    if requests_list:
        await message.answer(f'Список запросов:\n<b>{requests_list}</b>',
                             parse_mode='html',
                             reply_markup=await Main_Admin_Menu())
    else:
        await message.answer("Список запросов пуст.")
    await entry_log(message.from_user.full_name, "ввел команду GetRequests - администратор\n")


async def Cmd_Add_User(message: types.Message):
    await message.answer("Введите никнейм пользователя, которому вы хотите предоставить пользовательский доступ.")
    await Admins.admin_add_user.set()
    await entry_log(message.from_user.full_name, "ввел команду AddUser - администратор\n")

async def Add_User(message: types.Message):
    if await Search_date_DB('requests', 'profile_name', message.text):
        user_id = await Add_New_Record('requests', 'users', message.text)
        await message.answer(f"Пользователю {message.text}, открыт пользовательский доступ!",
                             reply_markup=await Main_Admin_Menu())
        await message.bot.send_message(user_id, "Администратор открыл для вас пользовательский доступ в боте!\n"
                                                "Для того чтобы узнать какие функции доступны для вашего профиля"
                                                " отправьте команду /Help или команду /Menu для выбора команды.")
        await entry_log(message.from_user.full_name, f"открыл пользовательский доступ для "
                                                     f"{message.text}\n Пользователю {message.text} было"
                                                     f" отправлено сообщение- администратор\n")
        await Admins.admin.set()
    else:
        await message.answer("Пользователь с таким никнеймом не отправлял запрос в данном боте, попробуйте отправить"
                             " другой никнейм еще раз.")
        await entry_log(message.from_user.full_name, "ввел никнейм которого нет в списке запросов при добавлении"
                                                     "  пользователя - Администратор\n")


async def Cmd_Get_Users(message: types.Message):
    users_list = await get_datas_table('users')
    if users_list:
        await message.answer(f'Список пользователей:\n<b>{users_list}</b>',
                             parse_mode='html',
                             reply_markup=await Main_Admin_Menu())
    else:
        await message.answer("Список пользователей пуст.",
                             reply_markup=await Main_Admin_Menu())
    await entry_log(message.from_user.full_name, "ввел команду /GetUsers - Администратор\n")

async def Cmd_Delete_User(message: types.Message):
    await message.answer("Введите никнейм пользователя, которого вы хотите удалить.")
    await Admins.admin_delete_user.set()
    await entry_log(message.from_user.full_name, "отправил команду /DeleteUser - Администратор\n")


async def Delete_User(message: types.Message):

    if await Search_date_DB('users', 'profile_name', message.text):
        await Delete_Data('users', 'profile_name', message.text)
        await message.answer(f"Пользователь {message.text} успешно удален из списка пользователей.",
                             reply_markup=await Main_Admin_Menu())
        await Admins.admin.set()
        await entry_log(message.from_user.full_name, f"удалил пользователя {message.text} - Администратор")
    else:
        await message.answer("Пользователя с таким никнеймом нет в списке пользователей, попробуйте отправить"
                             " другой никнейм еще раз.")
        await entry_log(message.from_user.full_name, "ввел никнейм которого нет в списке пользователей при удалении"
                                                     "  пользователя - Администратор\n")


async def Cmd_Add_Admin(message: types.Message):
    await message.answer("Вы хотите добавить администратора из списка:",
                         reply_markup=await add_admin_inline_keyboard())
    await Admins.admin_input_nick_new_admin.set()
    await entry_log(message.from_user.full_name, "отправил команду /AddAdmin - Администратор\n")


async def Input_Nick_Admin(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['table'] = callback.data
    await callback.message.edit_text("Введите никнейм пользователя, которого вы хотите добавить в качестве"
                                     " Администратора")
    await Admins.admin_add_new_admin
    await entry_log(callback.message.from_user.full_name, "выбрал от куда добавить нового администратора и ввел"
                                                          " никнейм пользователя для добавления - Администратор\n")


async def Add_Admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if await Search_date_DB(data['table'], 'profile_name', message.text):
            user_id = await Add_New_Record(data['table'], 'admins', message.text)
            await message.answer(f"Пользователю {message.text}, открыт администраторский доступ доступ!",
                                 reply_markup=await Main_Admin_Menu())
            await message.bot.send_message(user_id, "Администратор открыл для вас администраторский доступ в боте!\n"
                                                    "Для того чтобы узнать какие функции доступны для вашего профиля"
                                                    " отправьте команду /Help или команду /Menu для выбора команды.")
            await entry_log(message.from_user.full_name, f"открыл администраторский доступ для "
                                                         f"{message.text}\n Пользователю {message.text} было"
                                                         f" отправлено сообщение - администратор\n")
            await Admins.admin.set()
        else:
            await message.answer(
                "Пользователь с таким никнеймом нету в списке, попробуйте отправить"
                " другой никнейм еще раз.")
            await entry_log(message.from_user.full_name, "ввел никнейм которого нет в cписке при добавлении"
                                                         "  пользователя - Администратор\n")


async def Cmd_Change_Token(message: types.Message):
    pass


async def Get_Empty_Report(message: types.Message):
    await message.answer_document(open(f'C:\\pythonProject\\New_Wialon\\empty_report\\Пустой отчет.xlsx', 'rb'),
                                  caption=f'Пустой отчет для заполнения.\nЗаполните в нем столбцы'
                                  f' B, C, L и M, послего чего отправьте команду /FillReport'
                                  f' и отправьте боту отчет для заполнения.',
                                  reply_markup=await Main_Admin_Menu())
    await entry_log(message.from_user.full_name, "отправил команду /EmptyReport и получил пустой отчет"
                                                 " - Администратор\n")


async def Cmd_Menu(message: types.Message):
    await message.answer("Выберете команду!",
                         reply_markup=await Main_Admin_Menu())
    await entry_log(message.from_user.full_name, "отправил команду /Menu - Администратор\n")


async def Cmd_Help(message: types.Message):
    await message.answer(Main_Admin_Menu_Text,
                         parse_mode='html')
    await entry_log(message.from_user.full_name, "отправил команду /Help - Администратор\n")


async def Cmd_Stop(message: types.Message):
    await message.answer("Действие выбранное вами ранее было остановленно.")
    await Admins.admin.set()
    await entry_log(message.from_user.full_name, "остановил выбранное ранее дествие - Администратор\n")


async def Message_Not_Info(message: types.Message):
    await message.answer("Дождитесь пока отчет будет заполнен, после чего вы сможете отправлять команды.\n"
                         "Либо отправьте команду /Stop для остановки заполнения отчета.")
    await entry_log(message.from_user.full_name, "отправил сообщение во время заполнения отчет - Администратор\n")


async def Message_No_Cmd(message: types.Message):
    await message.answer("К сожалению такой команды не существует, попробуйте отправить другую команду"
                         " или выберите команду из меню.",
                         reply_markup=await Main_Admin_Menu())
    await entry_log(message.from_user.full_name, "отправил не существующую команду - Администратор\n")


def register_handler(dp: Dispatcher):
    dp.register_message_handler(Cmd_Get_Requests,
                                commands=['GetRequests'],
                                state=Admins.admin)
    dp.register_message_handler(Cmd_Add_User,
                                commands=['AddUser'],
                                state=Admins.admin)
    dp.register_message_handler(Add_User,
                                state=Admins.admin_add_user)
    dp.register_message_handler(Cmd_Get_Users,
                                commands=['GetUsers'],
                                state=Admins.admin)
    dp.register_message_handler(Cmd_Delete_User,
                                commands=['DeleteUser'],
                                state=Admins.admin)
    dp.register_message_handler(Delete_User,
                                state=Admins.admin_delete_user)
    dp.register_message_handler(Cmd_Add_Admin,
                                commands=['AddAdmin'],
                                state=Admins.admin)
    dp.register_message_handler(Input_Nick_Admin,
                                state=Admins.admin_input_nick_new_admin)
    dp.register_message_handler(Add_Admin,
                                state=Admins.admin_add_new_admin)
    dp.register_message_handler(Cmd_Change_Token,
                                commands=['ChangeToken'],
                                state=Admins.admin)
    dp.register_message_handler(Get_Empty_Report,
                                commands=['EmptyReport'],
                                state=Admins.admin)
    dp.register_message_handler(Cmd_Menu,
                                commands=['Menu'],
                                state=Admins.admin)
    dp.register_message_handler(Cmd_Help,
                                commands=['Help'],
                                state=Admins.admin)
    dp.register_message_handler(Message_Not_Info,
                                state=Admins.admin_send_file)
    dp.register_message_handler(Message_No_Cmd,
                                state=Admins.admin)


def register_callback_handler(dp: Dispatcher):
    dp.register_callback_query_handler(Add_Admin,
                                       lambda c: c.data.startswith('requests', 'users'))
