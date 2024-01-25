import pytest

from tests.conftest import *

pytestmark = pytest.mark.asyncio


# async def test_empty_database(async_client: AsyncClient) -> None:
#     response = await async_client.delete("db_manager/empty_database")
#     assert response.status_code == 204


# async def test_seed_database(async_client: AsyncClient) -> None:
#     response = await async_client.post("/db_manager/seed")
#     assert response.status_code == 200
