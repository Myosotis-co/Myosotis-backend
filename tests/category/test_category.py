import pytest
from fastapi.testclient import TestClient

from tests.confest import (
    client,
    get_test_db,
    create_test_database,
    url,
    test_db_session as db,
)
from app.category.models import *

# client = TestClient(app)


# Create Category
test_category = {"user_id": 2, "temp_email_id": 2, "category_name": "Pytest data"}
test_category_2 = {"user_id": 3, "temp_email_id": 3, "category_name": "Pytest data 2"}


# @pytest.fixture(scope="function")
# @pytest.mark.asyncio
# def test_create_category():
#     try:
#         response = next(client()).post("/category/create", json=test_category)
#         assert response.status_code == 201
#     finally:


class TestCategory:
    def setup(self):
        self.category_url = "/category"

    @pytest.fixture(autouse=True)
    def test_create_data(self, db):
        db.add(test_category)
        db.commit()
        db.refresh(test_category)

    def test_404(self, client, db):
        response = client.get("/category")
        assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_create_another_category():
#     try:
#         response = client.post("/category/create", json=test_category_2)
#         assert response.status_code == 201
#     finally:
#         testing_session.rollback()

# # Get Category
# @pytest.mark.asyncio
# async def test_get_category():
#     response = client.get("/category/get/1")
#     assert response.status_code == 200
#     assert response


# @pytest.mark.asyncio
# async def test_get_category_fail():
#     response = client.get("/category/get/0")
#     assert response.status_code == 404
