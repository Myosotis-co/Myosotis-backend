from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.db_manager.seeder import *
from app.db_manager.db_manage import *

router = APIRouter(tags=["DB_Manager"])


@router.post("/seed", status_code=200)
async def seed_database(session: AsyncSession = Depends(get_async_session)):
    try:
        await database_seeding(session)
        return "Seeding completed"
    except Exception as e:
        # Handle the exception and return an appropriate error response
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/empty_database", status_code=204)
async def empty_database(session: AsyncSession = Depends(get_async_session)):
    try:
        await database_emptying(session)
        return "Database is emptied"
    except Exception as e:
        # Handle the exception and return an appropriate error response
        raise HTTPException(status=500, detail=str(e))
