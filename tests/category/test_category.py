import pytest

from tests.confest import *
from app.category.models import *

pytestmark = pytest.mark.asyncio


# Create Category
test_category = {"user_id": 2, "temp_email_id": 1, "category_name": "Pytest data"}
test_category_2 = {"user_id": 3, "temp_email_id": 2, "category_name": "Pytest data 2"}


async def test_create_another_category(async_client: AsyncClient) -> None:
    response = await async_client.post("/category/create", json=test_category_2)
    assert response.status_code == 201


async def test_create_category(async_client: AsyncClient) -> None:
    response = await async_client.post("/category/create", json=test_category)
    assert response.status_code == 201


async def test_get_category(async_client: AsyncClient) -> None:
    response = await async_client.get("/category/get/1")
    assert response.status_code == 200


# # Get Category
# @pytest.mark.asyncio
# @pytest.fixture
# async def async_example_orm(async_db: AsyncSession) -> Category:
#     category = Category(
#         user_id=1,
#         temp_email_id=1,
#         category_name="Test category",
#     )
#     async_db.add(category)
#     await async_db.commit()
#     await async_db.refresh()
#     return category


# @pytest.mark.asyncio
# async def test_get_category_fail():
#     response = client.get("/category/get/0")
#     assert response.status_code == 404
