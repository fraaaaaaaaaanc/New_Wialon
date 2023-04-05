import openpyxl
import datetime


def data_collection(file_name):

    all_cars_datas_from_excel, one_car_datas = [], []

    book = openpyxl.open(file_name)
    sheet = book.active

    print(sheet.max_row)
    cells = sheet["B8": f"B{sheet.max_row}"]

    for cell in cells:
        for el in cell:
            print(str(el.value))

data_collection("C:\\pythonProject\\New_Wialon\\doc.xlsx")