from abc import ABC
from typing import Type

from sqlalchemy.orm import Session

from nexusdata.legacy.repositories import SimpleSessionRepository


class RepositoryContext(ABC):

    def __init__(self, session:Session):
        self._session = session
        self.__setup_repositories__()

    def __setup_repositories__(self):
        fields:list[tuple[str, Type[SimpleSessionRepository]]] = [(name, cls) for name, cls in self.__class__.__annotations__.items() if self.__is_repository__(cls)]
        for name, cls in fields:
            setattr(self, name, cls(self._session))

    @staticmethod
    def __is_repository__(cls) -> bool:
        return isinstance(cls, type) and issubclass(cls, SimpleSessionRepository)