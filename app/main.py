from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.evaluation import router as evaluation_router
from app.api.interview import router as interview_router

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/frontend/static"),
    name="static"
)

#подключаем стиль

app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

# Инициализируем роутеры для API
app.include_router(evaluation_router)
app.include_router(interview_router)


# Templates for frontend
templates = Jinja2Templates(directory="app/frontend")

# Роуты для отображения HTML страницы
@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profession.html", response_class=HTMLResponse)
async def profession_page(request: Request):
    return templates.TemplateResponse("profession.html", {"request": request})

@app.get("/select-persona", response_class=HTMLResponse)
async def select_persona_page(request: Request):
    return templates.TemplateResponse("select-candidate.html", {"request": request})

@app.get("/interview", response_class=HTMLResponse)
async def interview_page(request: Request):
    return templates.TemplateResponse("interview.html", {"request": request})

@app.get("/evaluation", response_class=HTMLResponse)
async def evaluation_page(request: Request):
    return templates.TemplateResponse("evaluation.html", {"request": request})

@app.get("/report", response_class=HTMLResponse)
async def report_page(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})
