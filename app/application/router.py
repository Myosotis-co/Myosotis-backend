from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.application.schema import *
# from app.application.functions import *

router = APIRouter(tags=["Application"])