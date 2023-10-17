import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    pass


class CategoryCreate(BaseModel):
    user_id: int
    temp_email_id: int
    category_name: str


class Category(CategoryBase):
    id: int
    user_id: int
    temp_email_id: int
    category_name: str
    deletion_date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class CategoryUpdate(CategoryBase):
    temp_email_id: int = None
    category_name: str = None
