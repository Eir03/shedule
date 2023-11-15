import glob
import json
import os
import openpyxl
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session

from db_models import *

source_folder = r'excel_files' #Можно в конфиг добавить
extension = 'xlsx'

def sortBy():
    path = getLastFile(source_folder)
    wb = openpyxl.load_workbook(path)
    sheet = wb.active
    groups = []
    coordinate = []
    schedule = []

    for cell in sheet[3]:
        if cell.value:
            coordinate.append(cell.coordinate)
            groups.append(cell.value)

    groups = [x.replace('группа', '').replace(' ', '') for x in groups]
    groups_dict = dict(zip(groups, coordinate))

    week_type = ['Нечетная', 'Четная']
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

    for week in week_type:
        for group in groups_dict:
            cell = sheet[groups_dict[group]]
            cell = sheet[cell.row + 3][cell.column - 1]

            for day_index, day in enumerate(days):
                for i in range(5):
                    number = cell.value
                    subject = sheet[cell.row][cell.column + 1].value
                    teach = sheet[cell.row + 1][cell.column + 1].value
                    cabinet = sheet[cell.row][cell.column + 4].value

                    if week == 'Нечетная':
                        if type(sheet[cell.row][cell.column + 2].value) is int:
                            cabinet = sheet[cell.row][cell.column + 2].value
                    else:
                        if sheet[cell.row][cell.column + 2].value is not None:
                            subject = sheet[cell.row][cell.column + 3].value
                            teach = sheet[cell.row + 1][cell.column + 3].value
                    if subject is None:
                        cabinet = None
                    period = {
                        "group": group,
                        "number": number,
                        "subject": subject.replace('\n', ' ') if subject is not None else '',
                        "teacher": teach.replace('\n', ' ').replace('     ', '') if teach is not None else '',
                        "cabinet": cabinet,
                        "day": day_index + 1,
                        "week_type": week
                    }
                    schedule.append(period)
                    cell = sheet[cell.row + 2][cell.column - 1]
    save_to_database(schedule)

def save_to_database(data):

    db_file = 'ooooooooooooo.db'
    if os.path.exists(db_file):
        os.remove(db_file)

    engine = create_engine(f'sqlite:///{db_file}', echo=True)
    model.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for period in data:
            # Получаем или создаем объекты WeekType, Group, Teacher и Discipline
            week_type = session.query(WeekType).filter_by(name=period["week_type"]).first()
            if not week_type:
                week_type = WeekType(name=period["week_type"])
                session.add(week_type)

            group = session.query(Group).filter_by(name=period["group"]).first()
            if not group:
                group = Group(name=period["group"])
                session.add(group)

            teacher = session.query(Teacher).filter_by(name=period["teacher"]).first()
            if not teacher and period["teacher"] != '':
                teacher = Teacher(name=period["teacher"])
                session.add(teacher)

            discipline = None
            if period["subject"] is not None and period["subject"] != '':
                discipline = session.query(Discipline).filter_by(name=period["subject"]).first()
                if not discipline:
                    discipline = Discipline(name=period["subject"])
                    session.add(discipline)
                # Добавим discipline в сессию, чтобы получить id
                session.flush()

            # Добавляем запись в таблицу Schedule
            schedule_entry = Schedule(
                id_week_type=week_type.id,
                id_group=group.id,
                id_teacher=teacher.id if teacher else None,
                id_discipline=discipline.id if discipline else None,
                day=period["day"],
                number=period["number"],
                cabinet=period["cabinet"],
            )
            session.add(schedule_entry)

        # Сохраняем изменения в базе данных
        session.commit()
        print("Данные успешно записаны в базу данных!")

    except Exception as e:
        session.rollback()
        print(f"Ошибка при записи данных в базу данных: {e}")

    finally:
        session.close()

def getLastFile(source_folder):
    if not os.path.isdir(r'excel_files'):
        os.mkdir(source_folder)
    list_files = [os.path.join('', file_name) for file_name in glob.glob(f"{source_folder}/*.{extension}")]
    list_files = sorted(list_files, key=lambda x: x[0])
    if not list_files:
        raise FileNotFoundError(f"Файл с таким расширением не найден")
    return list_files[0]
