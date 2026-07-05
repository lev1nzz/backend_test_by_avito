
import re
import string

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import ValueUrl
from src.main import CreateUrlSchema, UrlSchema
from src.shortener import generate_short_url


def create_short_url_service(payload: CreateUrlSchema, db: Session = Depends(get_db)):
    
    if not payload.url or payload.url.strip() == '':
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='URL can`t be emtpy'
        )
    
    
    all_chars = list(string.ascii_letters + string.digits)
    
    while True:
        short_slug = generate_short_url(all_chars)
        slug_exists = db.query(ValueUrl).filter(
            ValueUrl.short_url == short_slug).first()

        if not slug_exists:
            break
            
            # добавление урла в таблицу бд
    new_url = ValueUrl(short_url=short_slug, base_url=payload.url)
        
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
            
    return UrlSchema(
        id=new_url.id,
        short_url=new_url.short_url,
        url=new_url.base_url)



def url_by_slug(short_slug: str, db: Session = Depends(get_db)):
    return db.query(ValueUrl).filter(
        ValueUrl.short_url == short_slug).first()

def get_original_url_service(short_slug: str, db: Session = Depends(get_db)):
    url_entry = url_by_slug(db, short_slug)
    
    if not url_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
        )

    return url_entry.base_url