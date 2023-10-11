import datetime
from pydantic import BaseModel

from app.category.schema import Category


class TempEmailBase(BaseModel):
    email: str


class TempEmailCreate(BaseModel):
    pass


class TempEmail(TempEmailBase):
    id: int
    access_token: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    category: Category
