from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.application.schema import *
from app.application.functions import *

router = APIRouter(tags=["Application"])

@router.post("/applications/create")
async def create_applications(
    category_id: int,
    website_url: str,
    session: AsyncSession = Depends(get_async_session),
):
    service_add_application(category_id,website_url,session)
    try:
        await session.commit()
        return {"status": 201, "data": "Application is created"}
    except Exception as e:
        return "Failed to create application: " + str(e)
