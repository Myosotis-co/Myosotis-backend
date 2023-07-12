
import random
from fastapi import APIRouter, Depends, HTTPException

from app import crud, fake_generator, schema
from app.database import get_db
from sqlalchemy.orm import Session

from app.models.Landmark import Landmark
from app.models.User import User


router = APIRouter()

@router.get("/landmarks/{landmark_id}", response_model=schema.Landmark)
def get_landmark(landmark_id: int, db: Session = Depends(get_db)):
    db_landmark = crud.get_landmark(db=db, landmark_id=landmark_id)
    if db_landmark is None:
        raise HTTPException(status_code=404,detail="Landmark not found")
    return db_landmark


@router.post("/generate_landmark", response_model=schema.Landmark)
def create_landmark(landmark: schema.LandmarkCreate, db: Session = Depends(get_db)):
    user_random = random.randint(0,db.query(User).count()-1)
    landmarks = fake_generator.generate_fake_landmarks(1,user_random)
    landmark = Landmark(**landmarks[0])
    db.add(landmark)
    db.commit()
    db.refresh(landmark)
    return landmark

