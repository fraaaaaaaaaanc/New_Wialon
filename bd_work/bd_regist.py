import sqlite3 as sq


async def db_start():  # Подключение к базе дыннх и создание таблиц
    global db, cur

    db = sq.connect('wialon.db')
    cur = db.cursor()

    return cur


async def Search_date_DB(table, **kwargs): # функция проверяющая есть ли аккаунт у пользователя начавшего работу с ботом

    cur = await db_start()

    if cur.execute(f"""SELECT "{list(kwargs.keys())[0]}" FROM '{table}' 
    WHERE "{list(kwargs.keys())[0]}" == '{kwargs['user_id']}'""").fetchall():
        db.close()
        return True
    db.close()
    return False

async def Add_Data_DB(table, **kwargs):

    cur = await db_start()

    if not cur.execute(f"""SELECT "{list(kwargs.keys())[0]}" FROM {table}
     WHERE "{list(kwargs.keys())[0]}" == '{kwargs['user_id']}'""").fetchall():
        cur.execute(f"""INSERT INTO {table} ('user_id', 'profile_name') 
        VALUES ('{kwargs['user_id']}', '{kwargs['profile_name']}')""")
        db.commit()
    else:
        db.close()
        return False
    db.close()
    return True

get

async def Get_Datas(table, *args):

    cur = await db_start()
    data_list = {}
    result_id = cur.execute(f"""SELECT "{args[0]}" FROM {table}""").fetchall()
    result_name = cur.execute(f"""SELECT "{args[1]}" FROM {table}""").fetchall()
    for id, name in zip(result_id, result_name):
        data_list[id[0]] = name[0]

    db.close()
    return data_list