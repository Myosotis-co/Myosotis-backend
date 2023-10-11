import datetime
from app.category.schema import Category
from pydantic import BaseModel


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
