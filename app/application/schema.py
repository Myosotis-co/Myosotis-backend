import datetime
from typing import List
from pydantic import BaseModel
from app.message.schema import Message


class ApplicationBase(BaseModel):
    pass


class ApplicationCreate(BaseModel):
    pass


class Application(ApplicationBase):
    id: int
    category_id: int
    website_url: str
    deletion_date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime

    receivedMessages: List[Message]


class ApplicationUpdate(ApplicationBase):
    website_url: str = None
