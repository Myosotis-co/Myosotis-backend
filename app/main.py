import os
from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fastapi_users
from app.auth.models import User


from app.auth.schema import UserCreate, UserRead
from app.config import settings

from app import seeder
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware
from app.auth.jwt_config import auth_backend,fastapi_users
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

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

current_user = fastapi_users.current_user()

#Added for test
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.name}"


#app.include_router(user.router,tags=["Users"],prefix="/api/users")

