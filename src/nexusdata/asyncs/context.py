from abc import ABC
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from nexusdata.asyncs.repositories import AsyncSessionRepository


class AsyncRepositoryContext(ABC):

    def __init__(self, session:AsyncSession):
        self._session = session
        self.__setup_repositories__()

    def __setup_repositories__(self):
        fields:list[tuple[str, Type[AsyncSessionRepository]]] = [(name, cls) for name, cls in self.__class__.__annotations__.items() if self.__is_repository__(cls)]
        for name, cls in fields:
            setattr(self, name, cls(self._session))

    @staticmethod
    def __is_repository__(cls) -> bool:
        return isinstance(cls, type) and issubclass(cls, AsyncSessionRepository)