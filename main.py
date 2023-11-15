import time

from parser import *
from fastapi import FastAPI, Path
from db_models import *
app = FastAPI(
    title='schedule 26 kadr'
)

@app.get('/')
def main():
    return ''
@app.get('/update')
def update_schedule():
    parse()
    return "OK"

@app.get('/students')
def get_schedule():
    engine = create_engine(f'sqlite:///{db_file}', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session.query(Schedule).all()

@app.get('/teacher/{teacher_id}')
def schedule_by_teacher(teacher_id:int):
    return teacher_id

@app.get('/group/{group_id}')
def schedule_by_group(group_id: int):
    return