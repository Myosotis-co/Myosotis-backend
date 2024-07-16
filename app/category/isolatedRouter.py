from app.auth.models import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.category.schema import *
from app.category.models import Category as Category_model
from app.crud_manager import *
from app.auth.jwt_config import fastapi_users


current_user = fastapi_users.current_user(active=True)

routerCategory = APIRouter(tags=["isolatedCategory"])

@routerCategory.get("/get/{category_id}")
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    try:
        category = await service_get_model(Category_model, category_id, session)

        currentUserID = user.id
        userCategoryId = category.user_id
        if currentUserID == userCategoryId:
            if category is not None:
                return category
        raise HTTPException(status_code=404, detail="Category not found")
    except Exception as e:
        return "Failed to get a category: " + str(e)

