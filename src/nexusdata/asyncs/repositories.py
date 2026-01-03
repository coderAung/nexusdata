from abc import ABC

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from nexusdata.core.metadata.typings import MODEL, ID
from nexusdata.utils.abstractions import AbstractRepository


class AsyncSessionRepository(AbstractRepository[MODEL, ID], ABC):

    def __init__(self, session:AsyncSession):
        super().__init__()
        self._session = session

    async def save(self, entity:MODEL) -> MODEL:
        self._session.add(entity)
        await self._session.flush([entity])
        return entity

    async def save_all(self, entities:list[MODEL]) -> list[MODEL]:
        self._session.add_all(entities)
        await self._session.flush(entities)
        return entities

    async def find_by_id(self, _id:ID) -> MODEL:
        return await self._session.get(self._model, _id)

    async def count(self) -> int:
        return (await self._session.execute(select(func.count()).select_from(self._model))).scalar()

    async def delete(self, entity:MODEL):
        await self._session.delete(entity)

    async def delete_by_id(self, _id:ID):
        e = self.find_by_id(_id)
        await self._session.delete(e)