import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    pass


class CategoryCreate(BaseModel):
    pass


class Category(CategoryBase):
    id: int
    user_id: int
    temp_email_id: int
    category_name: str
    deletion_date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    # temp_email: ForwardRef("TempEmail")
    # applications: List[Application]

    class Config:
        orm_mode = True


class CategoryUpdate(CategoryBase):
    temp_email_id: int = None
    category_name: str = None
