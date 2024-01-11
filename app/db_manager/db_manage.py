import sqlalchemy as sa
from sqlalchemy.future import select
from sqlalchemyseed import load_entities_from_csv, Seeder
from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext

from app.database import get_async_session
from app.auth.models import Role, User
from app.category.models import Category
from app.email.models import TempEmail
from app.application.models import Application
from app.message.models import Message, Message_Type 

async def database_emptying(db):
    return