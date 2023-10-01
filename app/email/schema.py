import datetime
from app.category.schema import Category
from pydantic import BaseModel


class Temp_EmailBase(BaseModel):
    email: str


class Temp_EmailCreate(BaseModel):
    pass


class Temp_Email(Temp_EmailBase):
    id: int
    access_token: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    category: Category
