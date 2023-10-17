from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel

from app.database import get_async_session
from app.database import Base


async def service_create_model(
    defaul_model: Base,
    create_schema: BaseModel,
    session: AsyncSession = Depends(get_async_session),
):
    new_model = defaul_model()
    for key, value in create_schema:
        if value is not None:
            setattr(new_model, key, value)

    session.add(new_model)
    session.commit()

    return new_model


async def service_get_model(
    default_model: Base,
    model_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    exec_command = select(default_model).filter(default_model.id == model_id)
    result_value = await session.execute(exec_command)
    model = result_value.scalar()

    return model


async def service_update_model(
    model: Base,
    model_update: BaseModel,
    session: AsyncSession = Depends(get_async_session),
):
    for key, value in model_update:
        if value is not None:
            setattr(model, key, value)
    session.add(model)
    return model
