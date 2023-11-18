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
from tests.confest import async_db, async_db_engine, async_client,generate_email


pytestmark = pytest.mark.asyncio



async def test_email(async_client: AsyncClient, async_db: AsyncSession,generate_email:TempEmail_model):
    assert generate_email.email == 'test@gmail.com'

