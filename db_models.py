from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

model = declarative_base()

class WeekType(model):
    __tablename__ = 'week_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Group(model):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cource = Column(Integer)

class Discipline(model):
    __tablename__ = 'discipline'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Teacher(model):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Schedule(model):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    id_week_type = Column(Integer, ForeignKey(WeekType.id))
    id_group = Column(Integer, ForeignKey(Group.id))
    id_teacher = Column(Integer, ForeignKey(Teacher.id))
    id_discipline = Column(Integer, ForeignKey(Discipline.id))
    day = Column(String(20), nullable=False)
    number = Column(Integer, nullable=False)
    cabinet = Column(String(50))