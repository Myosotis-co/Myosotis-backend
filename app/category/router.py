from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.category.schema import *
from app.category.models import Category as Category_model
from app.crud_manager import *

router = APIRouter(tags=["Category"])


@router.post("/create", status_code=201)
async def create_category(
    category_create: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_category = await service_create_model(Category_model, category_create, session)
    if new_category is not None:
        return "New category is created"
    raise HTTPException(status_code=418, detail="Failer to create a category")


@router.get("/get/{category_id}", status_code=200)
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    category = await service_get_model(Category_model, category_id, session)
    if category is not None:
        return category
    raise HTTPException(status_code=404, detail="Category not found")


@router.patch("/update/{category_id}", status_code=201)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    category = await service_get_model(Category_model, category_id, session)
    if category is not None:
        service_update_model(category, category_update, session)
        await session.commit()
        return "Category is updated"
    raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/delete/{category_id}", status_code=202)
async def delete_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    await service_delete_model(Category_model, category_id, session)
    await session.commit()
    return "Category is deleted"


@router.get("/get_all", status_code=200)
async def get_categories(
    page_num: int,
    items_per_page: int,
    session: AsyncSession = Depends(get_async_session),
):
    categories = await service_get_some_models(
        Category_model, page_num, items_per_page, session
    )
    return categories
