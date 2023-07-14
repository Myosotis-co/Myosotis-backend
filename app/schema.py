
from datetime import datetime
from typing import List

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    # role_id: int
    is_deleted: bool
    name: str
    email: str
    user_token: str

    class Config:
        orm_mode = True
    
# class Role(BaseModel):
#     id: int
#     name: str
#     description: str

#     class Config:
#         orm_mode = True