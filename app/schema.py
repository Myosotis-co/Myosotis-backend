from typing import List
from pydantic import BaseModel
from app.category.schema import *


class MessageBase(BaseModel):
    pass


class MessageCreate(BaseModel):
    pass


class Message(MessageBase):
    id: int
    application_id: int
    message_type_id: int
    topic: str
    message_text: str
    created_at: datetime.datetime


# ---#
class Message_TypeBase(BaseModel):
    pass


class Message_TypeCreate(BaseModel):
    pass


class Message_Type(Message_TypeBase):
    id: int
    name: str
    topic: str

    messages: List[Message]


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
