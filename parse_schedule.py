import glob
import json
import os
import openpyxl
from Levenshtein import distance as levenshtein

from config import source_folder, db_file, extensions, week_type, days
from db_models import *

def parse_schedule():
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

                    if day_index == 3 and week == 'Четная':
                        pass

                    if week == 'Нечетная':
                        if type(sheet[cell.row][cell.column + 2].value) is int:
                            cabinet = sheet[cell.row][cell.column + 2].value
                    elif week == 'Четная':
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
    if os.path.exists(db_file):
        os.remove(db_file)

    engine = create_engine(f'sqlite:///{db_file}')
    model.metadata.create_all(engine)
    session = create_session()

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
            # teacher_name = period["teacher"]
            # existing_teachers = session.query(Teacher).all()
            #
            # # Проверяем, есть ли уже преподаватель с похожим именем
            # matching_teachers = [teacher for teacher in existing_teachers if
            #                      levenshtein(teacher.name, teacher_name) <= 2]
            # if teacher_name != '':
            #     if matching_teachers:
            #         # Если есть преподаватель с похожим именем, используем его
            #         teacher = matching_teachers[0]
            #     else:
            #         # Иначе создаем нового преподавателя
            #         teacher = Teacher(name=teacher_name)
            #         session.add(teacher)

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
    if not os.path.isdir(source_folder):
        os.mkdir(source_folder)
        return
    list_files = [os.path.join('', file_name) for file_name in glob.glob(f"{source_folder}/*.{extensions}")]
    list_files = sorted(list_files, key=lambda x: x[0])
    if not list_files:
        raise FileNotFoundError(f"Файл с таким расширением не найден")
    return list_files[0]
