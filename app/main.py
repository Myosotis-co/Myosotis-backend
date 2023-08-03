import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app import crud
from app.config import settings
from app.models import User
from app.routers import user
from app.routers import emails

from app import seeder
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware
from app.database import SQLALCHEMY_DATABASE_URL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "/docker/env/.env-docker"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)

origins = [
    settings.CLIENT_ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, tags=["Users"], prefix="/functions/users")
app.include_router(emails.router)
