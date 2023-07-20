from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import crud
from app.config import settings
from app.database import  engine
from app import models
from app.routers import user
from app.seeder import seed

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN
]

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router,tags=["Users"],prefix="/api/users")
seed()