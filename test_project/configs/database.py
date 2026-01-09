from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel, select

import test_project.models
from test_project.models.account import Account
from test_project.models.role import Role

from test_project.utils.singletons import password_hasher

engine = create_async_engine(
    url="sqlite+aiosqlite:///./social.db",
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSessionLocal() as session:
        role_count = (await session.execute(select(func.count()).select_from(Role))).scalar()
        account_count = (await session.execute(select(func.count()).select_from(Account))).scalar()
        commit = False
        if role_count == 0:
            session.add_all([Role(name="admin"), Role(name="member")])
            commit = True
        if account_count == 0:
            session.add(Account(
                name="admin",
                email="admin@gmail.com",
                password=password_hasher.hash("admin"),
                role_id=1,
            ))
            commit = True
        if commit:       
            await session.commit()

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
