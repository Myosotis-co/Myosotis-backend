from app.auth.models import User
from app.permissions import check_user_access
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.message.schema import *
from app.message.models import Message as Message_model
from app.crud_manager import *
from app.auth.jwt_config import fastapi_users

current_user = fastapi_users.current_user(active=True)
router = APIRouter(tags=["Message"], dependencies=[Depends(current_user)])


@router.post("/create")
async def create_message(
    message_create: MessageCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        await service_create_model(Message_model, message_create, session)
        await session.commit()
        return {"status": 201, "data": "Message is created"}
    except Exception as e:
        return "Failed to create message: " + str(e)


@router.get("/get/{message_id}")
async def get_message(
    message_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        message = await service_get_model(Message_model, message_id, session)
        if message is not None:
            if not check_user_access(user, message):
                return HTTPException(status_code=403, detail="Forbidden")
            return message
        raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        return "Failed to get a message: " + str(e)


@router.patch("/{message_id}")
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        message = await service_get_model(Message_model, message_id, session)
        if message is not None:
            if not check_user_access(user, message):
                return HTTPException(status_code=403, detail="Forbidden")
            await service_update_model(message, message_update, session)
            await session.commit()
            return {"status": 204, "data": "Message is updated"}
        raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        return "Failed to update a message: " + str(e)


@router.delete("/delete/{message_id}")
async def delete_message(
    message_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        message = await service_get_model(Message_model, message_id, session)
        if message is not None:
            if not check_user_access(user, message):
                return HTTPException(status_code=403, detail="Forbidden")
            await service_delete_model(Message_model, message_id, session)
            await session.commit()
            return {"status": 204, "data": "Message is deleted"}
    except Exception as e:
        return "Failed to delete a message: " + str(e)


@router.get("/get_all")
async def get_messages(
    page_num: int,
    items_per_page: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        messages = await service_get_some_models(
            Message_model, page_num, items_per_page, session
        )
        validated_messages = []
        for message in messages:
            if check_user_access(user, message):
                validated_messages.append(message)
        return messages
    except Exception as e:
        return "Failed to get messages: " + str(e)
