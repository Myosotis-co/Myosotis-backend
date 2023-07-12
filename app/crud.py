from sqlalchemy.orm import Session

from app import  schema
from app.fake_generator import generate_fake_users
from app.models.Landmark import Landmark
from app.models.Route import Route
from app.models.User import User

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_landmark(db: Session, landmark_id: int):
    return db.query(Landmark).filter(Landmark.id == landmark_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_landmarks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Landmark).offset(skip).limit(limit).all()

def get_routes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Route).offset(skip).limit(limit).all()

def get_route(db: Session, route_id: int):
    return db.query(Route).filter(Route.id == route_id).first()

def create_user(db: Session, user: schema.UserCreate):
    db_user = User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_landmark(db: Session, landmark: schema.LandmarkCreate, user_id: int):
    db_landmark = Landmark(**landmark.dict(), user_id=user_id)
    db.add(db_landmark)
    db.commit()
    db.refresh(db_landmark)
    return db_landmark

def create_route(db: Session, route: schema.RouteCreate, user_id: int):
    db_route = Route(**route.dict(), user_id=user_id)
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

def get_landmark_by_user_id(db: Session, user_id: int):
    return db.query(Landmark).filter(Landmark.user_id == user_id).all()

def get_route_by_user_id(db: Session, user_id: int):
    return db.query(Route).filter(Route.user_id == user_id).all()
