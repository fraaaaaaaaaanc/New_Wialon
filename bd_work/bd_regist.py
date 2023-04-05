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

async def Add_Data_DB(table, column, data):

    cur = await db_start()

    if not cur.execute(f"""SELECT "{column}" FROM {table} WHERE "{column}" == '{data}'""").fetchall():
        cur.execute(f"""INSERT INTO {table} ('{column}') VALUES ('{data}')""")
        db.commit()
        db.close()
        return True
    db.close()
    return False