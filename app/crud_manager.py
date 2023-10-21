from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select, delete
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


async def service_add_model(
    model: Base,
    session: AsyncSession = Depends(get_async_session),
):
    session.add(model)
    session.commit()
    return model


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


async def service_delete_model(
    default_model: Base,
    model_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    exec_command = delete(default_model).filter(default_model.id == model_id)
    await session.execute(exec_command)


async def service_get_some_models(
    default_model: Base,
    page: int,
    items_per_page: int,
    session: AsyncSession = Depends(get_async_session),
):
    # Calculate the offset to retrieve the appropriate chunk
    offset = (page - 1) * items_per_page

    # Sort by a stable column like 'created_at'
    exec_command = (
        select(default_model)
        .order_by(desc(default_model.created_at))
        .limit(items_per_page)
        .offset(offset)
    )

    result_value = await session.execute(exec_command)
    models = result_value.all()

    return models
