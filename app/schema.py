
from datetime import datetime
from typing import List

from pydantic import BaseModel

class LandmarkBase(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float
    image: str
    user_id: int

class LandmarkCreate(LandmarkBase):
    pass


class RouteBase(BaseModel):
    name: str
    description: str
    user_id: int

class RouteCreate(RouteBase):
    pass

class Route(RouteBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

    def __init__(self, **data):
        super().__init__(**data)
        self.landmarks: List[Landmark] = []

class Landmark(LandmarkBase):
    id: int
    user_id: int
   
    class Config:
        orm_mode = True
    
    def __init__(self, **data):
        super().__init__(**data)
        self.routes: List[Route] = []


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
        self.landmarks = []
        self.routes = []