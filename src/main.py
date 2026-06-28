
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, status
from fastapi.responses import RedirectResponse
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



