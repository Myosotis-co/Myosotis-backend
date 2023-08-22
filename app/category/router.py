from fastapi import APIRouter, Depends, HTTPException

from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.category.models import Category

router = APIRouter(tags=["Category"])


@router.get("/categories/{category_id}")
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    exec_command = select(Category).filter(Category.id == category_id)
    result_value = await session.execute(exec_command)
    category = result_value.scalar()

    return {category}


# @router.post("/create_category", response_model=Category)
# async def seeder_post(
#     post: CategoryCreate, session: AsyncSession = Depends(get_async_session)
# ):
#     try:
#         await create_category(post, session)
#         return {"status": 201, "data": "Category created"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/categories")
# async def create_category(
#     category: Category, session: AsyncSession = Depends(get_async_session)
# ):
#     try:
#         await category_creation(category, session)
#         return {"status": 200, "data": "Category created"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
