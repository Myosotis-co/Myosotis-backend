
from datetime import datetime
from typing import List

from pydantic import BaseModel




class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str
    is_active: bool

    class Config:
        orm_mode = True
    
    def __init__(self, **data):
        super().__init__(**data)
        