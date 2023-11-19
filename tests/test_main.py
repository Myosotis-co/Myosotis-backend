import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.email.models import TempEmail as TempEmail_model

pytestmark = pytest.mark.asyncio


async def test_email(generate_email: TempEmail_model):
    assert generate_email.email == "test@gmail.com"
