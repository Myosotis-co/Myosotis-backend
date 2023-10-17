import datetime
from typing import ForwardRef, List
from pydantic import BaseModel


class MessageBase(BaseModel):
    pass


class MessageCreate(BaseModel):
    application_id: int
    message_type_id: int
    topic: str
    message_text: str


class Message(MessageBase):
    id: int
    application_id: int
    message_type_id: int
    topic: str
    message_text: str
    created_at: datetime.datetime


class MessageUpdate(MessageBase):
    message_type_id: int
    topic: str
    message_text: str


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
