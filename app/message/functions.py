from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_async_session
from app.message.models import Message
from app.message.schema import Message as MessageSchema


async def service_get_message(
    message_id: int, session: AsyncSession = Depends(get_async_session)
):
    exec_command = select(Message).filter(Message.id == message_id)
    result_value = await session.execute(exec_command)
    message = result_value.scalar()

    return message