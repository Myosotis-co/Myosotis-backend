import pytest, asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings
from app.database import SQLALCHEMY_DATABASE_URL
from app.main import app
from app.database import Base

@pytest.fixture(scope="session")
def client():
    yield TestClient(app=app)
    

# @pytest.fixture(scope="session")
# def tmp_database():
#     try:
#         engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
#         testing_session = sessionmaker(
#             expire_on_commit=False,
#             autocommit=False,
#             autoflush=False,
#             bind=engine,
#             class_=AsyncSession,
#         )
#     catch Exception as e:


# @pytest.fixture

# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
# testing_session = sessionmaker(
#     expire_on_commit=False,
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
#     class_=AsyncSession,
# )

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# asyncio.run(init_models())


# def override_get_db():
#     try:
#         db = testing_session()
#         yield db
#     finally:
#         db.close()


# client = TestClient(app)

# app.dependency_overrides[get_db] = override_get_db


# @pytest.fixture
# async def async_db_engine():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     yield engine

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(scope="function")
# async def async_db(async_db_engine):
#     async_session = sessionmaker(
#       expire_on_commit=False,
#       autocommit=False,
#       autoflush=False,
#       bind=async_db_engine,
#       class_=AsyncSession,
#     )

#     async with async_session() as session:
#         await session.begin()

#         yield session

#         await session.rollback()

#         for table in reversed(Base.metadata.sorted_tables):
#             await session.execute(f"TRUNCATE {table.name} CASCADE;")
#             await session.commit()


# @pytest.fixture
# async def async_client() -> AsyncClient:
#     return AsyncClient(app=app, base_url="http://localhost")


# @pytest.fixture
# async def generate_email(async_db: AsyncSession):
#     email = TempEmail(email="test@gmail.com")
#     async_db.add(email)
#     await async_db.commit()
#     await async_db.refresh(email)
#     return email
