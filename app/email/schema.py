import datetime
from pydantic import BaseModel

from typing import List

from app.category.schema import Category

from pydantic import EmailStr

class EmailSchema(BaseModel):
    email: List[EmailStr]

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
