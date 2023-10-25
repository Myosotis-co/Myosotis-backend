import datetime
from pydantic import BaseModel

from app.category.schema import Category


class TempEmailBase(BaseModel):
    email: str
    access_token: str


class TempEmailCreate(BaseModel):
    email: str
    access_token: str


class TempEmail(TempEmailBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    category: Category


class TempEmailUpdate(BaseModel):
    email: str
    access_token: str
