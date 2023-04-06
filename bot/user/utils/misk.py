from bot.state import Users, Admins


Main_User_Menu_Text = '''
<b>/EmptyReport</b> - <em>Команда для получения примера пустого отчета.</em>
<b>/FillReport</b> - <em>Команда для заполнения отчета.</em>
<b>/Menu</b> - <em>Команда для получения меню.</em>
<b>/Stop</b> - <em>Команда для остановки выбранного действия.</em>
'''


state_list = [Users.user,
              Users.user_send_file]