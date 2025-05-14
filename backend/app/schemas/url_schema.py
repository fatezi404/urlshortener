from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class URLLong(BaseModel):
    long_url: HttpUrl

    class Config:
        orm_mode = True

class URLShort(BaseModel):
    short_url: str 

    class Config:
        orm_mode = True

class URLResponse(URLLong, URLShort):
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class URLUpdate(BaseModel):
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True