from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_async_session

async def service_create_model(
    defaul_model,
    create_schema,
    session: AsyncSession = Depends(get_async_session),
):
    new_model = defaul_model()
    for key, value in create_schema:
        if value is not None:
            setattr(new_model, key, value)

    session.add(new_model)
    session.commit()

    return new_model