import sqlite3 as sq


async def db_start():  # Подключение к базе дыннх и создание таблиц
    global db, cur

    db = sq.connect('wialon.db')
    cur = db.cursor()

    return cur


async def Search_date_DB(table, column, data): # функция проверяющая есть ли аккаунт у пользователя начавшего работу с ботом

    cur = await db_start()

    if cur.execute(f"""SELECT "{column}" FROM '{table}' WHERE "{column}" == '{data}'""").fetchall():
        db.close()
        return True
    db.close()
    return False


async def Add_Data_DB(table, **kwargs):

    cur = await db_start()
    for key, value in kwargs.items():
        print(key, value)
        if cur.execute(f"""SELECT "{key}" FROM {table} WHERE "{key}" == '{value}'""").fetchall():
            db.close()
            return False
    cur.execute(f"""INSERT INTO {table} ('user_id', 'profile_name') 
    VALUES ('{kwargs['user_id']}', '{kwargs['profile_name']}')""")
    db.commit()
    db.close()
    return True


async def Get_Column(table, column):

    cur = await db_start()
    datas = []
    result = cur.execute(f"""SELECT "{column}" FROM {table}""").fetchall()
    for el in result:
        datas.append(el[0])

    db.close()
    return datas


async def Get_Str_Datas(table, column, data):

    cur = await db_start()
    datas = []
    result = cur.execute(f"""SELECT * FROM {table} WHERE {column}=='{data}'""").fetchall()
    for el in result[0]:
        datas.append(el)

    db.close()
    return datas


async def Get_Data(table, *args):

    cur = await db_start()
    result = cur.execute(f"""SELECT {args[0]} FROM {table} WHERE {args[1]} = '{args[2]}'""").fetchone()
    return result[0]

async def Delete_Data(table, *args):

    cur = await db_start()
    cur.execute(f"""DELETE from {table} WHERE "{args[0]}" == '{args[1]}'""").fetchall()
    db.commit()
    db.close()