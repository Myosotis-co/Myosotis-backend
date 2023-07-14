from typing import List
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role_id: int
    is_deleted: bool
    name: str
    email: str
    user_token: str

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    pass

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    title: str
    description: str
    users: List[User] = []

    class Config:
        orm_mode = True