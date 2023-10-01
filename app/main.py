import os
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

# from app import email
from app.auth.models import User
from app.auth.schema import UserCreate, UserRead
from app.config import settings
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware
from app.auth.jwt_config import auth_backend, fastapi_users, google_oauth_client, reddit_oauth_client, linkedin_oauth_client, github_oauth_client
from app.database import SQLALCHEMY_DATABASE_URL
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from app.email.router import router as email_router
from app.seeder.router import router as seeder_router
from app.category.router import router as category_router


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
    email_router,
    prefix="/email",
    tags=["Email"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, "SECRET", redirect_url="http://localhost:8000"),
    prefix="/auth/google",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_oauth_router(linkedin_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/linkedin",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_oauth_router(github_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/github",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_oauth_router(reddit_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/reddit",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(seeder_router, prefix="/seeder", tags=["Seeder"])

app.include_router(category_router, prefix="/category", tags=["Category"])

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
