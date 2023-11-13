class Schedule:
    def __init__(self, monday, wednesday, friday, saturday, sunday):
        self.monday = monday
        self.wednesday = wednesday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday

class Day:
    def __init__(self, lessons):
        self.lessons = lessons

class Lesson:
    def __init__(self, number, subject, teacher, cabinet):
        self.number = number
        self.subject = subject
        self.teacher = teacher
        self.cabinet = cabinet

def from_json(json_object):
    monday = Day([Lesson(**lesson) for lesson in json_object["понедельник"]["уроки"]])
    wednesday = Day([Lesson(**lesson) for lesson in json_object["среда"]["уроки"]])
    friday = Day([Lesson(**lesson) for lesson in json_object["пятница"]["уроки"]])
    saturday = Day([Lesson(**lesson) for lesson in json_object["суббота"]["уроки"]])
    sunday = Day([Lesson(**lesson) for lesson in json_object["воскресенье"]["уроки"]])

    return Schedule(monday, wednesday, friday, saturday, sunday)