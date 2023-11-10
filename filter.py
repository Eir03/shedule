import glob
import os
import openpyxl

source_folder = r'excel_files' #Можно в конфиг добавить
extension = 'xlsx'

def sortBy():
    path = getLastFile()
    wb = openpyxl.load_workbook(path)
    sheet = wb.active
    groups = []
    coordinate = []
    for cell in sheet[3]:
        if cell.value:
            coordinate.append(cell.coordinate)
            groups.append(cell.value)
    groups = [x.replace('группа', '').replace(' ', '') for x in groups]
    groups_dict = dict(zip(groups, coordinate))
    print(groups_dict)
    for group in groups_dict:
        cell = sheet[groups_dict[group]]
        cell = cell.offset(1, 0)
        print(cell)




def getLastFile():
    if not os.path.isdir(r'excel_files'):
        os.mkdir(source_folder)
    list_files = [os.path.join('', file_name) for file_name in glob.glob(f"{source_folder}/*.{extension}")]
    list_files = sorted(list_files, key=lambda x: x[0])
    if not list_files:
        raise FileNotFoundError(f"Файл с таким расширением не найден")
    return list_files[0]
