import time
from collections import defaultdict

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from config import db_file, extensions, days
from parse_schedule import parse_schedule
from fastapi import FastAPI, Path
from db_models import *

app = FastAPI(
    title='schedule 26 kadr'
)
templates = Jinja2Templates(directory="templates")

# Роут для открытия HTML-страницы с передачей данных
@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    session = create_session()
    query = select(Group)
    result = session.execute(query).fetchall()

    groups = [row[0] for row in result]

    session.close()

    return templates.TemplateResponse('group.html', {"request": request, "groups": groups, "days": days})

@app.get('/update')
def update_schedule():
    parse_schedule()
    return "OK"

@app.get('/students')
def get_schedule():
    session = create_session()
    return session.query(Schedule).all()

@app.get('/teacher/{teacher_id}')
def schedule_by_teacher(teacher_id:int):
    return teacher_id

@app.get('/groups/', response_class=HTMLResponse)
def schedule_by_group(request: Request, group_id=1):
    session = create_session()

    result = session.execute(select(Schedule).filter(Schedule.id_group == group_id)).fetchall()
    group_query = session.execute(select(Group)).fetchall()
    groups = [row[0] for row in group_query]

    session.close()
    return templates.TemplateResponse('group.html', {"request": request, "result": result, "days": days, 'groups':groups})

@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def create_session():
    engine = create_engine(f'sqlite:///{db_file}')
    Session = sessionmaker(bind=engine)
    return Session()