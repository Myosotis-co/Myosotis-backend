from fastapi import APIRouter, Depends, HTTPException

from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.category.models import Category

router = APIRouter(tags=["Category"])


@router.get("/categories/get/{category_id}")
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    exec_command = select(Category).filter(Category.id == category_id)
    result_value = await session.execute(exec_command)
    category = result_value.scalar()

    return category


@router.put("/categories/update/{category_id}")
async def update_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    return {"status": 204, "data": "Category is updated"}
    # exec_command = select(Category).filter(Category.id == category_id)
    # result_value = await session.execute(exec_command)
    # category = result_value.scalar()

    # await session.commit()


# Relocate this function to function.py
def add_category(
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


@router.post("/categories/create")
async def create_category(
    user_id: int,
    temp_email_id: int,
    category_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    new_category = add_category(user_id, temp_email_id, category_name, session)
    try:
        await session.commit()
        return new_category
    except Exception as e:
        return "Failed to create new category: {e}"
    # except IntegrityError as ex:
    #     await session.rollback()
    #     raise DuplicatedEntryError("Such a category already exist!")


@router.delete("/categories/delete/{category_id}")
async def delete_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    # Try #4
    # session.query()

    # Try #3
    # exec_command = select(Category).filter(Category.id == category_id)
    # result_value = await session.execute(exec_command)
    # category = result_value.scalar()

    # await session.delete(category)

    # Tries #1 and #2
    # sql_query = "DELETE FROM categories WHERE categories.id = " + str(
    #     category_id
    # )  # Not working :(

    # exec_command = delete(Category).where(Category.id == category_id)
    # sql_query = str(exec_command)

    # session.delete()

    # print(sql_query)
    # await session.execute(sql_query)

    return {"status": 200, "data": "Category is deleted"}
