
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import  engine
from sqlalchemy.orm import Session

from src.database.db import get_db, engine
from src.database.models import Base
from src.schemas import CreateUrlSchema, UrlSchema
from src.service import create_short_url_service, get_original_url_service



# создание таблиц при запуске сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Используем правильный способ создания таблиц
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    yield


app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory="static"), name="static")


# ===== UI ЭНДПОИНТ =====
@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница с UI для сокращения ссылок"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head><title>Ошибка</title></head>
            <body>
                <h1>⚠️ Файл static/index.html не найден</h1>
                <p>Пожалуйста, создайте файл static/index.html с UI интерфейсом</p>
            </body>
            </html>
        """, status_code=404)


# ручка добавления в бд короткого и длинного урла
@app.post('/short_url')
def create_short_url(
    payload: CreateUrlSchema, db: Session = Depends(get_db)
    ) -> UrlSchema: return create_short_url_service(payload, db)
    

@app.get('/{short_slug}')
def redirect_to_short_url(short_slug: str, db: Session = Depends(get_db)):
    
    original_url = get_original_url_service(db, short_slug)
    return RedirectResponse(
        url=original_url, status_code=status.HTTP_301_MOVED_PERMANENTLY
    )



