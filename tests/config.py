import pytest_asyncio
import uuid
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api import router as api_router
from models import BaseOrm
from db import get_session


@pytest_asyncio.fixture(scope="session")
async def engine_session(tmp_path_factory):
    # SQLite database URL for testing
    db_path = tmp_path_factory.getbasetemp() / "test.db"
    SQLITE_DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

    # Create a SQLAlchemy engine
    engine = create_async_engine(
        SQLITE_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create a sessionmaker to manage sessions
    TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.create_all)

    return engine, TestingSessionLocal


@pytest_asyncio.fixture(scope="session")
async def db_session(engine_session):
    """Create a new database session with a rollback at the end of the test."""
    connection = await engine_session[0].connect()
    session = engine_session[1](bind=connection)
    yield session
    await session.close()
    await connection.close()


@pytest_asyncio.fixture(scope="session")
async def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_session():
        try:
            yield db_session
        finally:
            db_session.close()
    app = FastAPI()
    app.include_router(
        api_router,
        prefix="/api/v1"
    )

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app, base_url="http://127.0.0.1:8000/api/v1") as test_client:
        yield test_client
