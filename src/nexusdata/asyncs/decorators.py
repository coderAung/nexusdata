from functools import wraps
from typing import Callable, Any, Awaitable, Type

from sqlalchemy import RowMapping, text
from sqlalchemy.ext.asyncio import AsyncSession

from nexusdata.core.metadata.typings import DTO
from nexusdata.asyncs.uow.transactions import do_trx
from nexusdata.utils.exceptions import NexusQueryException
from nexusdata.utils.queries.resolvers import resolve_result
from nexusdata.utils.queries.utilities import is_collection
from nexusdata.utils.singletons import nexus_query_generator


def transactional(func:Callable[..., Awaitable[Any]] | None = None, *, read_only:bool = False):
    def decorator(fn:Callable[..., Awaitable[Any]]):
        @wraps(fn)
        async def wrapper(self, *args, **kwargs):
            session:AsyncSession = getattr(self, "_session")

            depth = getattr(self, "__trx_depth__", 0)
            self.__trx_depth__ = depth + 1

            async def call_func():
                return await fn(self, *args, **kwargs)
            try:
                result = await do_trx(call_func, session, depth, read_only)
                return result
            finally:
                self.__trx_depth__ -= 1
        return wrapper

    if func is None:
        return decorator
    return decorator(fn=func)

def query(
        func:Callable[..., Awaitable[Any]] | None = None,
        *, sql:str | None = None,
        dto:Type[DTO] | None = None,
        map_func:Callable[[RowMapping], DTO] | None = None):

    if func is None and sql is None:
        raise NexusQueryException("func or sql must be defined to use query.")

    async def query_func(self, *args, **kwargs):
        nq = nexus_query_generator.generate_query(func, self._model, *args, **kwargs)
        session:AsyncSession = getattr(self, "_session")
        stmt = nq.query.where(text(nq.where))
        result = await session.execute(statement=stmt, params=nq.params)
        if nq.is_count: return result.scalar()
        if nq.is_delete: return None

        rt = func.__annotations__.get("return", None)
        if is_collection(rt):
            return result.scalars().all()
        return result.scalar_one_or_none()

    def decorator(fn:Callable[..., Any]):
        # noinspection PyUnresolvedReferences
        @wraps(fn)
        async def wrapper(self, *args, **kwargs):
            session:AsyncSession = getattr(self, "_session")

            annotations:dict[str, Any] = fn.__annotations__.copy()
            if annotations.__contains__("return"):
                annotations.pop("return")

            params = nexus_query_generator.generate_params(list(annotations.keys()), *args, **kwargs)
            result = (await session.execute(statement=text(sql), params=params)).mappings()

            rt = fn.__annotations__.get("return", None)
            return resolve_result(result=result, dto=dto, map_func=map_func, rt=rt)
        return wrapper

    if func is None:
        return decorator
    return query_func
