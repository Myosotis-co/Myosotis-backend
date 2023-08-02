
import datetime
from typing import List, Optional
from typing import List, Optional
from typing import List, Optional

from app.schema import Category,UserBase
from fastapi_users import schemas

from app.schema import Category,UserBase


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    role_id: int
    is_deleted: bool = False
    is_active: bool = True
    is_verified: bool = False

    class Config:
        orm_mode = True

class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    role_id: int = 2
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False