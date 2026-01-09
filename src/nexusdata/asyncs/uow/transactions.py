from collections.abc import Awaitable
from typing import Callable, Any

from sqlalchemy.ext.asyncio import AsyncSession


async def do_trx(func:Callable[[], Awaitable[Any]], session:AsyncSession, depth:int, read_only:bool):
    try:
        result = await func()
        if depth == 0:
            if read_only:
                session.expunge_all()
                await session.rollback()
            else:
                await session.commit()
        return result
    except Exception as e:
        await session.rollback()
        raise e