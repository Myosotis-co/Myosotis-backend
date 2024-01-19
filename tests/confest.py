import pytest, asyncio
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Session

from app.database import SQLALCHEMY_DATABASE_URL
from app.main import app
from app.database import *


url = str(SQLALCHEMY_DATABASE_URL + "_test")
_db_conn = create_async_engine(url)


def get_test_db_conn():
    assert _db_conn is not None
    return _db_conn


def get_test_db():
    session = AsyncSession(bind=_db_conn)

    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    if database_exists(url):
        drop_database(url)
    create_database(url)
    # Base.metadata.create_async_engine(_db_conn) # Create the tables.
    Base.metadata.create_all(_db_conn)
    # app.dependency_overrides[get_db] = get_test_db  # Mock the Database Dependency
    app.dependency_overrides[get_async_session] = get_test_db
    yield
    drop_database(url)


@pytest.yield_fixture
def test_db_session():
    session = Session(bind=_db_conn)
    yield session
    for table in reversed(Base.metadata.sorted_tables):
        _db_conn.execute(table.delete())
    session.close()


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client
