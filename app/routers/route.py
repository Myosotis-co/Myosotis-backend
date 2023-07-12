


import random
from fastapi import APIRouter, Depends, HTTPException

from app import crud, fake_generator, schema
from app.database import get_db
from sqlalchemy.orm import Session

from app.models.Route import Route
from app.models.User import User


router = APIRouter()
@router.post("/generate_route", response_model=schema.Route)
def create_route(route: schema.RouteCreate, db: Session = Depends(get_db)):
    user_random = random.randint(0,db.query(User).count()-1)
    routes = fake_generator.generate_fake_routers(1,user_random)
    route = Route(**routes[0])
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

@router.get("/routes/{route_id}", response_model=schema.Route)
def get_route(route_id: int, db: Session = Depends(get_db)):
    db_route = crud.get_route(db=db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404,detail="Route not found")
    return db_route



