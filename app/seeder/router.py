from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.seeder.seeder import *

router = APIRouter(tags=["Seeder"])


@router.post("/seed")
async def seeder_post(session: AsyncSession = Depends(get_async_session)):
    try:
        await seed(session)
        return {"status": 200, "data": "Seed completed"}
    except Exception as e:
        # Handle the exception and return an appropriate error response
        raise HTTPException(status_code=500, detail=str(e))
