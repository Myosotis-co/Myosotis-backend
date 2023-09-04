from fastapi import APIRouter, Depends, HTTPException
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema import *
from app.category.functions import *

router = APIRouter(tags=["Category"])


@router.post("/categories/create")
async def create_category(
    user_id: int,
    temp_email_id: int,
    category_name: str,
    session: AsyncSession = Depends(get_async_session),
):
    new_category = service_add_category(user_id, temp_email_id, category_name, session)
    try:
        await session.commit()
        return {"status": 201, "data": "Category is created"}
    except Exception as e:
        return "Failed to create new category: " + str(e)


@router.get("/categories/get/{category_id}")
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        category = await service_get_category(category_id, session)
        if category is not None:
            return category
        raise HTTPException(status_code=404, detail="Category not found")
    except Exception as e:
        return "Failed to get a category: " + str(e)


# TODO: Create function to get list of categories as JSON
# @router.get("/categories/get/list", response_model=list[Schema_category])
# @router.get("/categories/get/list")
# async def get_categories(session: AsyncSession = Depends(get_async_session)):
#     categories = await service_get_categories(session)
#     # return [Schema_category(id = category.id) for category in categories]
#     return categories


# To implement
@router.patch("/categories/update/{category_id}")
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        category = await service_get_category(category_id, session)
        if category is not None:
            service_update_category(category, category_update, session)
            await session.commit()
            return {"status": 204, "data": "Category is updated"}
        raise HTTPException(status_code=404, detail="Category not found")
    except Exception as e:
        return "Failed to get a category: " + str(e)


# To implement
# @router.delete("/categories/delete/{category_id}")
# async def delete_category(
#     category_id: int, session: AsyncSession = Depends(get_async_session)
# ):
#     # Try #4
#     # session.query()

#     # Try #3
#     # exec_command = select(Category).filter(Category.id == category_id)
#     # result_value = await session.execute(exec_command)
#     # category = result_value.scalar()

#     # await session.delete(category)

#     # Tries #1 and #2
#     # sql_query = "DELETE FROM categories WHERE categories.id = " + str(
#     #     category_id
#     # )  # Not working :(

#     # exec_command = delete(Category).where(Category.id == category_id)
#     # sql_query = str(exec_command)

#     # session.delete()

#     # print(sql_query)
#     # await session.execute(sql_query)

#     return {"status": 200, "data": "Category is deleted"}
