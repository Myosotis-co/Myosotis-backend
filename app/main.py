import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# from app import email
from app.auth.models import User
from app.auth.schema import UserCreate, UserRead
from app.config import settings
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware
from app.auth.jwt_config import auth_backend, fastapi_users
from app.database import SQLALCHEMY_DATABASE_URL

from fastapi.openapi.docs import get_swagger_ui_html

from fastapi.staticfiles import StaticFiles

from app.email.router import router

from app.seeder.router import router as seeder_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "/docker/env/.env-docker"))

app = FastAPI(docs_url=None, title="DeleteMeHere")
app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [settings.CLIENT_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router,
    prefix="/email",
    tags=["Email"],
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
app.include_router(seeder_router, tags=["Seeder"])

current_user = fastapi_users.current_user()


# Added for test
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.name}"


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html_cdn():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        # swagger_ui_dark.css CDN link
        swagger_css_url="/static/swagger_ui_dark.css",
    )


# app.include_router(user.router,tags=["Users"],prefix="/api/users")
