import time
from collections import defaultdict

import uvicorn
from sqlalchemy.orm import sessionmaker, joinedload, aliased, lazyload
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from config import db_file, extensions, days
from parse_schedule import parse_schedule
from fastapi import FastAPI, Path, HTTPException
from db_models import *

app = FastAPI(
    title='schedule 26 kadr'
)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)


templates = Jinja2Templates(directory="templates")

# Роут для открытия HTML-страницы с передачей данных
@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    session = create_session()
    result = session.query(Group).all()

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



@app.get('/groups/', response_class=HTMLResponse)
def redirect_to_groups(request: Request):
    return RedirectResponse(url='/groups/1')

@app.get('/groups/{group_id}', response_class=HTMLResponse)
def schedule_by_group(request: Request, group_id: int = 1):
    session = create_session()

    # schedule_query = session.query(select(Schedule).filter(Schedule.id_group == group_id)).fetchall()
    schedule_query = session.query(Schedule).options(joinedload(Schedule.discipline),
                                                     joinedload(Schedule.teacher)
                                                     ).filter(Schedule.id_group == group_id).all()
    even_week_schedule = []
    odd_week_schedule = []

    for row in schedule_query:
        if row.id_week_type == 1:
            odd_week_schedule.append(row)
        elif row.id_week_type == 2:
            even_week_schedule.append(row)

    groups = session.query(Group).all()
    group = session.query(Group).filter(Group.id == group_id).first()

    result = odd_week_schedule + even_week_schedule
    session.close()
    return templates.TemplateResponse('group.html',
                                      {'request': request, 'result': result,
                                       'days': days, 'groups': groups, 'group_name': group.name})

@app.get('/teachers/', response_class=HTMLResponse)
def redirect_to_groups(request: Request):
    return RedirectResponse(url='/teachers/1')

@app.get('/teachers/{teacher_id}', response_class=HTMLResponse)
def schedule_by_group(request: Request, teacher_id: int = 1):
    session = create_session()

    # schedule_query = session.query(select(Schedule).filter(Schedule.id_group == group_id)).fetchall()
    schedule_query = session.query(Schedule).options(joinedload(Schedule.discipline),
                                                     joinedload(Schedule.teacher)
                                                     ).filter(Schedule.id_teacher == teacher_id).all()
    even_week_schedule = []
    odd_week_schedule = []

    for row in schedule_query:
        if row.id_week_type == 1:
            odd_week_schedule.append(row)
        elif row.id_week_type == 2:
            even_week_schedule.append(row)

    groups = session.query(Group).all()
    group = session.query(Group).filter(Group.id == teacher_id).first()

    result = odd_week_schedule + even_week_schedule
    session.close()
    return templates.TemplateResponse('group.html',
                                      {'request': request, 'result': result,
                                       'days': days, 'groups': groups, 'group_name': group.name})




@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def convert_query(query):
    return [row[0] for row in query]