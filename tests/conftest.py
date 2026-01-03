import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from tests.domain.repos import AccountRepo

async_engine = create_async_engine(url="sqlite+aiosqlite:///./test.db", echo=True)

async_session_factory = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        print("Starting sessionndfakfdafdaf;l")
        yield session
        print("HERELLLLLLLLLLLLLLLLLLLLLLL")
        await session.rollback()

@pytest.fixture(autouse=True)
async def cleanup_asyncio_tasks():
    yield

    # Cancel all pending asyncio tasks
    pending = [
        task for task in asyncio.all_tasks()
        if task is not asyncio.current_task()
    ]

    for task in pending:
        task.cancel()

    await asyncio.gather(*pending, return_exceptions=True)

engine = create_engine("sqlite:///./test.db", echo=True)

@pytest.fixture()
def session():
    with sessionmaker(engine)() as _session:
        try:
            yield _session
        except Exception as e:
            _session.close()
            raise e

@pytest.fixture()
def account_repo(session:Session):
    return AccountRepo(session)