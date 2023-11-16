from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from config import db_file

model = declarative_base()

def create_session():
    engine = create_engine(f'sqlite:///{db_file}')
    Session = sessionmaker(bind=engine)
    return Session()

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
    group = relationship('Group', backref='schedule')
    id_teacher = Column(Integer, ForeignKey(Teacher.id))
    teacher = relationship('Teacher', backref='schedule')
    id_discipline = Column(Integer, ForeignKey(Discipline.id))
    discipline = relationship('Discipline', backref='schedule')
    day = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    cabinet = Column(String(50))

