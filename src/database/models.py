from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String

from src.config import BASE_URL_LEN, SHORT_URL_LEN



# базовый класс таблиц
class Base(DeclarativeBase): pass


# таблица для хранения данных
class ValueUrl(Base):
    __tablename__ = 'value_url'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    short_url = Column(String(SHORT_URL_LEN))
    base_url = Column(String(BASE_URL_LEN))
    
    
    def __repr__(self):
        return f"<ValueUrl(id={self.id}, short_url={self.short_url}, base_url={self.base_url})>"
    
    def __str__(self):
        return f"ValueUrl(short_url={self.short_url}, base_url={self.base_url})"