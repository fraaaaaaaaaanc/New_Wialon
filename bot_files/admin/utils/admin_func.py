from bd_work.bd_regist import Get_Column, Get_Data, Add_Data_DB, Delete_Data


async def get_datas_table(table):

    result_list = ''
    result_list_id = await Get_Column(table, 'user_id')
    result_list_name = await Get_Column(table, 'profile_name')
    for name, id in zip(result_list_name, result_list_id):
        result_list += f'{name}: {id}\n'

    return result_list


async def Add_New_Record(table_search, table_add, user_name):

    user_id = await Get_Data(table_search, 'user_id', 'profile_name', user_name)
    await Add_Data_DB(table_add, user_id=user_id, profile_name=str(user_name))
    await Delete_Data(table_search, 'profile_name', user_name)

    return user_id