import datetime
from typing import List
from pydantic import BaseModel

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

#---#
class Message_TypeBase(BaseModel):
    pass

class Message_TypeCreate(BaseModel):
    pass

class Message_Type(Message_TypeBase):
    id: int
    name: str
    topic: str

    messages: List[Message]

#---#
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

    # tempEmail: "Forward ref"
    # ListLoggerModel = ForwardRef("List[LoggerModel]")
    # LoggerModel.update_forward_refs()
    applications: List[Application]

    class Config:
        orm_mode = True

#---#
class Temp_EmailBase(BaseModel):
    email: str

class Temp_EmailCreate(BaseModel):
    pass

class Temp_Email(Temp_EmailBase):
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