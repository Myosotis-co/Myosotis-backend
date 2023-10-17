from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.message.schema import *
from app.message.functions import *
from app.functions import *

router = APIRouter(tags=["Message"])


@router.post("/messages/create")
async def create_message(
    message_create: MessageCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await service_create_model(Message, message_create, session)
    try:
        await session.commit()
        return {"status": 201, "data": "Message is created"}
    except Exception as e:
        return "Failed to create message: " + str(e)


@router.get("/messages/get/{message_id}")
async def get_message(
    message_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        message = await service_get_model(Message, message_id, session)
        if message is not None:
            return message
        raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        return "Failed to get a message: " + str(e)


@router.patch("/messages/{message_id}")
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        message = await service_get_model(Message, message_id, session)
        if message is not None:
            await service_update_model(message, message_update, session)
            await session.commit()
            return {"status": 204, "data": "Message is updated"}
        raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        return "Failed to update a message: " + str(e)


@router.delete("/messages/delete/{message_id}")
async def delete_message(
    message_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await service_delete_model(Message, message_id, session)
        await session.commit()
        return {"status": 204, "data": "Message is deleted"}
    except Exception as e:
        return "Failed to delete a message: " + str(e)


@router.get("messages/get_all")
async def get_messages(session: AsyncSession = Depends(get_async_session)):
    messages = await service_get_messages(session)
    return messages
