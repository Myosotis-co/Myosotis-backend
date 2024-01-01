from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.category.schema import *
from app.category.models import Category as Category_model
from app.crud_manager import *

router = APIRouter(tags=["Category"])


@router.post("/create")
async def create_category(
    category_create: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        await service_create_model(Category_model, category_create, session)
        await session.commit()
        return {"status": 201, "data": "Category is created"}
    except Exception as e:
        return "Failed to create a category: " + str(e)


@router.get("/get/{category_id}")
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    category = await service_get_model(Category_model, category_id, session)
    if category is not None:
        return category
    raise HTTPException(status_code=404, detail="Category not found")


@router.patch("/update/{category_id}")
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        category = await service_get_model(Category_model, category_id, session)
        if category is not None:
            service_update_model(category, category_update, session)
            await session.commit()
            return {"status": 204, "data": "Category is updated"}
        raise HTTPException(status_code=404, detail="Category not found")
    except Exception as e:
        return "Failed to update a category: " + str(e)


@router.delete("/delete/{category_id}")
async def delete_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        await service_delete_model(Category_model, category_id, session)
        await session.commit()
        return {"status": 204, "data": "Category is deleted"}
    except Exception as e:
        return "Failed to delete a category: " + str(e)


@router.get("/get_all")
async def get_categories(
    page_num: int,
    items_per_page: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        categories = await service_get_some_models(
            Category_model, page_num, items_per_page, session
        )
        return categories
    except Exception as e:
        return "Failed to get messages: " + str(e)
