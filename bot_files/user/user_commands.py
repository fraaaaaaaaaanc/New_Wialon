from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import os

from loging import entry_log
from bot_files.state import Users, Admins
from bot_files.keyboards import Main_User_Menu
from .utils import Main_User_Menu_Text
from completion_report.parsing import get_report


async def Cmd_Fill_Report(message: types.Message):
    await message.answer("Для начала работы с отчетом отправьте файл формата Excel.")
    await Users.user_send_file.set()
    await entry_log(message.from_user.full_name, "отправил команду /FillReport - Пользователь\n")


async def Fill_Report(message: types.Message):
    if message.document is None \
            or message.document.mime_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        await message.answer("Вы отправили файл неверного формата, файл должен быть Excel формата.\n"
                             "Отправьте файл еще раз.")
        await entry_log(message.from_user.full_name, "отправил файл неверного формата - Пользователь\n")
    else:
        destination_dir = "C:\\pythonProject\\New_Wialon\\reports"
        file_path = os.path.join(destination_dir, message.document['file_name'])
        await message.document.download(file_path)
        await message.answer("Это может занять какое то время.")
        if message.caption != None:
            result = get_report(message.caption, message.document.file_name)
        await message.answer_document(open(file_path, 'rb'))
        await Users.user.set()
        await entry_log(message.from_user.full_name, "получил заполненный отчет - Пользователь\n")


async def Get_Empty_Report(message: types.Message):
    await message.answer_document(open(f'C:\\pythonProject\\New_Wialon\\empty_report\\Пустой отчет.xlsx', 'rb'),
                                  caption=f'Пустой отчет для заполнения.\nЗаполните в нем столбцы'
                                  f' B, C, L и M, послего чего отправьте команду /FillReport'
                                  f' и отправьте боту отчет для заполнения.',
                                  reply_markup=await Main_User_Menu())
    await entry_log(message.from_user.full_name, "отправил команду /EmptyReport и получил пустой отчет"
                                                 " - Пользователь\n")


async def Cmd_Menu(message: types.Message):
    await message.answer("Выберете команду!",
                         reply_markup=await Main_User_Menu())
    await entry_log(message.from_user.full_name, "отправил команду /Menu - Пользователь\n")


async def Cmd_Help(message: types.Message):
    await message.answer(Main_User_Menu_Text,
                         parse_mode='html')
    await entry_log(message.from_user.full_name, "отправил команду /Help - Пользователь\n")


async def Cmd_Stop(message: types.Message):
    await message.answer("Действие выбранное вами ранее было остановленно.")
    await Users.user.set()
    await entry_log(message.from_user.full_name, "остановил выбранное ранее дествие - Пользователь\n")


async def Message_Not_Info(message: types.Message):
    await message.answer("Дождитесь пока отчет будет заполнен, после чего вы сможете отправлять команды.\n"
                         "Либо отправьте команду /Stop для остановки заполнения отчета.")
    await entry_log(message.from_user.full_name, "отправил сообщение во время заполнения отчет - Пользователь\n")


async def Message_No_Cmd(message: types.Message):
    await message.answer("К сожалению такой команды не существует, попробуйте отправить другую команду"
                         " или выберите команду из меню.",
                         reply_markup=await Main_User_Menu())
    await entry_log(message.from_user.full_name, "отправил не существующую команду - Пользователь\n")

async def User(message: types.Message):
    await Users.user.set()
    await message.answer("Тест профиля пользователя!")


def register_handler(dp: Dispatcher):
    dp.register_message_handler(Cmd_Fill_Report,
                                commands=['FillReport'],
                                state=[Users.user,
                                       Admins.admin])
    dp.register_message_handler(Fill_Report,
                                content_types=['document'],
                                state=Users.user_send_file)
    dp.register_message_handler(Get_Empty_Report,
                                commands=['EmptyReport'],
                                state=Users.user)
    dp.register_message_handler(Cmd_Menu,
                                commands=['Menu'],
                                state=Users.user)
    dp.register_message_handler(Cmd_Help,
                                commands=['Help'],
                                state=Users.user)
    dp.register_message_handler(Cmd_Stop,
                                state=Users.user_send_file)
    dp.register_message_handler(Message_Not_Info,
                                state=Users.user_send_file)
    dp.register_message_handler(Message_No_Cmd,
                                state=Users.user)
    dp.register_message_handler(User,
                                commands=['User'])