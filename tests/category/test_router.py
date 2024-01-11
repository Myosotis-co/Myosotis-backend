import pytest
from fastapi.testclient import TestClient

from app.category.schema import *
from tests.confest import client

# client = TestClient(app)


# Create Category
test_category = {"user_id": 2, "temp_email_id": 2, "category_name": "Pytest data"}
test_category_2 = {"user_id": 3, "temp_email_id": 3, "category_name": "Pytest data 2"}


@pytest.mark.asyncio
async def test_create_category():
    response = client.post("/category/create", json=test_category)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_another_category():
    response = client.post("/category/create", json=test_category_2)
    assert response.status_code == 201


# Get Category
@pytest.mark.asyncio
async def test_get_category():
    response = client.get("/category/get/1")
    assert response.status_code == 200
    assert response
    


@pytest.mark.asyncio
async def test_get_category_fail():
    response = client.get("/category/get/0")
    assert response.status_code == 404


