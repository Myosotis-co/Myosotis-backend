

from fastapi import APIRouter, Depends, HTTPException

from app import crud, schema
from app.database import get_db
from sqlalchemy.orm import Session

from app.fake_generator import generate_fake_users


router = APIRouter()

@router.get("/users/{user_id}", response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return db_user

@router.post("/users/add_user", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user = generate_fake_users(1)[0]
    return crud.create_user(db=db, user=user)
