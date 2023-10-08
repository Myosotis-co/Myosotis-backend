from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_async_session
from app.message.models import Message
from app.message.schema import Message as MessageSchema


def service_add_message(
    application_id: int,
    message_type_id: int,
    message_topic: str,
    message_text: str,
    session: AsyncSession = Depends(get_async_session),
):
    new_message = Message(
        application_id=application_id,
        message_type_id=message_type_id,
        message_topic=message_topic,
        message_text=message_text,
    )
    session.add(new_message)
    session.commit()
    return new_message


async def service_get_message(
    message_id: int, session: AsyncSession = Depends(get_async_session)
):
    exec_command = select(Message).filter(Message.id == message_id)
    result_value = await session.execute(exec_command)
    message = result_value.scalar()

    return message
