import datetime
from typing import Generic, List, Optional

from pydantic import BaseModel

from fastapi_users import schemas
from fastapi_users import models


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "oauth_accounts",
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})


class BaseUser(Generic[models.ID], CreateUpdateDictModel):
    """Base User model."""

    id: models.ID
    email: str
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserRead(BaseUser[int]):
    id: int
    email: str
    role_id: int
    is_deleted: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    email: str
    name: str
    password: str
    role_id: int = 2
    is_verified: Optional[bool] = False


class UserUpdate(CreateUpdateDictModel):
    email: str
    name: str
    password: str
    is_deleted: str
