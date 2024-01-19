from fastapi import Depends
from app.database import Base
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session


async def database_emptying(session: AsyncSession = Depends(get_async_session)):
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(f"TRUNCATE {table.name} CASCADE;")
        seq_name = table.name + "_id_seq"
        await session.execute(f"ALTER SEQUENCE {seq_name} RESTART WITH 1;")
        await session.commit()
