from pydantic import BaseModel


class UrlSchema(BaseModel):
    id: str
    short_url: str
    url: str


class CreateUrlSchema(BaseModel):
    url: str
    

class CreateCustomSlugSchema(BaseModel):
    url: str
    custom_slug: str