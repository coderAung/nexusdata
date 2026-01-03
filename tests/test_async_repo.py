import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.domain.models import Account, Post
from tests.domain.repos import AsyncAccountRepo, PostRepo


@pytest.mark.asyncio
async def test_post_repo(async_session:AsyncSession):
    repo = AsyncAccountRepo(async_session)
    a1 = Account(name="Aung Aung", email="aung@gmail.com", password="aungaung")
    a2 = Account(name="Su Su", email="su@gmail.com", password="susu")
    await repo.save(a1)
    await repo.save(a2)
    assert await repo.count() == 2

    assert (await repo.find_by_id(1)).name == "Aung Aung"
    assert (await repo.find_by_id(2)).name == "Su Su"

    post_repo = PostRepo(async_session)
    p1 = Post(content="Hello from Aung Aung.", account_id=1)
    p2 = Post(content="Hello from Aung Aung again.", account_id=1)
    p1 = await post_repo.save(p1)
    p2 = await post_repo.save(p2)
    assert p1._id == 1
    assert p2._id == 2
    print("Done test")
    return
