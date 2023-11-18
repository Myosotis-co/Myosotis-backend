from http.client import HTTPException
from app.auth.models import User
from app.auth.schema import UserCreate
from app.category.schema import CategoryCreate
from app.category.models import Category as Category_model
from app.email.models import TempEmail as TempEmail_model
from app.crud_manager import service_add_model, service_create_model, service_get_model
from app.email.schema import TempEmailCreate
from httpx import AsyncClient
import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from tests.confest import async_db, async_db_engine, async_client


pytestmark = pytest.mark.asyncio


async def test_create_category(async_client: AsyncClient, async_db: AsyncSession):
    temp_email_create = TempEmail_model(email='test@gmail.com')
    user_create = UserCreate(
        name="test",
        email=temp_email_create.email,
        password="test",
    )
    user =  service_create_model(User, user_create, async_db)

    temp_email_create.user_id = 1
    service_add_model(temp_email_create, async_db)

    category_create = CategoryCreate(
        category_name="Test d",
        temp_email_id=1,
        user_id=1
    )
    response = await async_client
    response = await response.post(
        "/category/categories/create", json=category_create.dict()
    )
    assert response.status_code == 200
    assert response.json() == {"status": 200, "data": "Category is created"}

    async with await async_db as session:
        
        category = await service_get_model(
            Category_model, category_create.name, session
        )
        assert category is not None

async def test_add_email(async_db: AsyncSession,async_client: AsyncClient,):
    email = TempEmail_model(email='test@gmail.com')
    async_db.add(email)
    await async_db.commit()
    await async_db.refresh(email)
    assert email.id == 1
