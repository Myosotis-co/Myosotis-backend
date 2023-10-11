from typing import List
from pydantic import BaseModel
from app.category.schema import Category


class UserBase(BaseModel):
    email: str


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


# ---#
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
