from aiogram.dispatcher.filters.state import StatesGroup, State


class Users(StatesGroup):

    user = State()
    user_send_file = State()


class Admins(StatesGroup):

    admin = State()
    admin_add_user = State()
    admin_delete_user = State()
    admin_input_nick_new_admin = State()
    admin_add_new_admin = State()
    admin_send_file = State()
