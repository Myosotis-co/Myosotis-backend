import datetime
from pydantic import BaseModel

from app.category.schema import Category


class TempEmailBase(BaseModel):
    email: str


class TempEmailCreate(BaseModel):
    email: str


class TempEmail(TempEmailBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    category: Category


class TempEmailUpdate(BaseModel):
    email: str
