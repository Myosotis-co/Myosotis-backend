import datetime
from typing import List
from pydantic import BaseModel

#---#
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

    class Config:
        orm_mode = True

#---#
class TempEmailBase(BaseModel):
    email: str

class TempEmailCreate(BaseModel):
    pass

class TempEmail(TempEmailBase):
    id : int
    access_token: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    category: Category

#---#
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role_id: int
    name: str
    user_token: str
    is_deleted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    categories: List[Category]

    class Config:
        orm_mode = True

#---#
class RoleBase(BaseModel):
    pass

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    name: str
    description: str
    users: List[User]

    class Config:
        orm_mode = True