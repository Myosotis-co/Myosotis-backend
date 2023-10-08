from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.message.schema import *
from app.message.functions import *

router = APIRouter(tags=["Message"])

@router.get("/messages/get/{message_id}")
async def get_message(
    message_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        message = await service_get_message(message_id, session)
        if message is not None:
            return message
        raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        return "Failed to get a message" + str(e)