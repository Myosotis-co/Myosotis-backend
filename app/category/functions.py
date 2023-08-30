from app.category.models import Category
from app.database import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


def service_add_category(
    user_id: int,
    temp_email_id: int,
    category_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    new_category = Category(
        user_id=user_id, temp_email_id=temp_email_id, category_name=category_name
    )
    session.add(new_category)
    return new_category


async def service_get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    exec_command = select(Category).filter(Category.id == category_id)
    result_value = await session.execute(exec_command)
    category = result_value.scalar()

    return category


# async def service_get_categories(session: AsyncSession) -> list[Category]:
#     result = await session.execute(select(Category).limit(10))
#     return result.scalar().all()
