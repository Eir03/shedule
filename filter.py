import glob
import json
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

    schedule = {}

    for cell in sheet[3]:
        if cell.value:
            coordinate.append(cell.coordinate)
            groups.append(cell.value)

    groups = [x.replace('группа', '').replace(' ', '') for x in groups]
    groups_dict = dict(zip(groups, coordinate))
    print(groups_dict)

    week_type = ['Нечетная', 'Четная']
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

    for week in week_type:
        schedule[week] = {}
        print(f"__________{week}__________")
        for group in trim_dict(groups_dict):
            cell = sheet[groups_dict[group]]
            cell = sheet[cell.row + 3][cell.column - 1]
            print()
            print(group)
            # Цикл по дням недели
            group_schedule = {}
            for day in days:
                group_schedule[day] = []
                print()
                print(day)
                #Цикл по парам
                for i in range(5):
                    number = cell.value
                    subject = sheet[cell.row][cell.column + 1].value
                    teach = sheet[cell.row + 1][cell.column + 1].value
                    cabinet = sheet[cell.row][cell.column + 4].value
                    if week == 'Нечетная':
                        if type(sheet[cell.row][cell.column + 2].value) is int:
                            cabinet = sheet[cell.row][cell.column + 2].value
                        if subject is None:
                            cabinet = None
                    else:
                        if sheet[cell.row][cell.column + 2].value is not None:
                            subject = sheet[cell.row][cell.column + 3].value
                            teach = sheet[cell.row + 1][cell.column + 3].value
                            if subject is None:
                                cabinet = None
                    period = {
                        "number": number,
                        "subject": subject.replace('\n', ' ') if subject is not None else '',
                        "teacher": teach,
                        "cabinet": cabinet
                    }
                    group_schedule[day].append(period)

                    print(number, subject.replace('\n', ' ') if subject is not None else '', teach, cabinet)
                    cell = sheet[cell.row + 2][cell.column - 1]
        schedule[week][group] = group_schedule
        break

    schedule_json = json.dumps(schedule, indent=4)
    with open("schedule.json", "w", encoding="utf-8") as f:
        f.write(schedule_json)

def getLastFile():
    if not os.path.isdir(r'excel_files'):
        os.mkdir(source_folder)
    list_files = [os.path.join('', file_name) for file_name in glob.glob(f"{source_folder}/*.{extension}")]
    list_files = sorted(list_files, key=lambda x: x[0])
    if not list_files:
        raise FileNotFoundError(f"Файл с таким расширением не найден")
    return list_files[0]

def trim_dict(d):
    return {key: value for key, value in list(d.items())[:1]}