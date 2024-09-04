import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.confest import (
    generate_email,
    async_db,
    async_db_engine,
    generate_user,
    generate_role,
)

from app.email.models import TempEmail as TempEmail_model

pytestmark = pytest.mark.asyncio


async def test_email(generate_email: TempEmail_model):
    assert generate_email.email == "test@gmail.com"


def test_good():
    assert 1 == 1


def test_loh():
    assert "loh" == "loh"
