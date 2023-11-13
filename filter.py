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
        # Получаем ячейку по координатам и смещаем ее на 2 вниз и 2 вправо
        cell = sheet[groups_dict[group]]
        cell = sheet[cell.row + 3][cell.column - 1]
        print(group)
        for i in range(5):
            number = cell.value
            subject = sheet[cell.row][cell.column + 1].value
            teach = sheet[cell.row + 1][cell.column + 1].value
            cabinet = sheet[cell.row][cell.column + 4].value
            print(number, subject.replace('\n', ' ') if subject is not None else '', teach, cabinet)
            cell = sheet[cell.row + 2][cell.column - 1]
        break





def getLastFile():
    if not os.path.isdir(r'excel_files'):
        os.mkdir(source_folder)
    list_files = [os.path.join('', file_name) for file_name in glob.glob(f"{source_folder}/*.{extension}")]
    list_files = sorted(list_files, key=lambda x: x[0])
    if not list_files:
        raise FileNotFoundError(f"Файл с таким расширением не найден")
    return list_files[0]
