import pytest
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_url() -> str:
    """Spin up a disposable Postgres container for the test session."""
    with PostgresContainer("postgres:15") as postgres:
        url = postgres.get_connection_url()
        # Replace psycopg2 driver with asyncpg for SQLAlchemy async
        yield url.replace("psycopg2", "asyncpg")


@pytest.fixture(name="session")
async def session_fixture(postgres_url: str) -> AsyncGenerator[AsyncSession, None]:
    """Provide a fresh Postgres DB session for each test."""
    engine = create_async_engine(postgres_url, future=True, echo=False)

    # Reset schema before each test
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
