import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# Get Category
@pytest.mark.anyio
async def test_get_category():
    response = client.get("/category/get/1")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_category_fail():
    response = client.get("/category/get/0")
    assert response.status_code == 404
