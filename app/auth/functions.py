from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from app.auth.models import User
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


# Get async db of the user
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
