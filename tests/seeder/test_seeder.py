# import pytest
# from fastapi.testclient import TestClient

# from app.db_manager.router import seed_database
# from tests.confest import client


# @pytest.mark.first
# @pytest.mark.asyncio
# def test_seeder_post():
#     response = client.post("/seeder/seed")
#     assert response.status == 200
#     assert response.data == "Seeding completed"
