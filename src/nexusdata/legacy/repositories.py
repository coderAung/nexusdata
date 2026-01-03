from abc import ABC

from sqlalchemy import func
from sqlalchemy.orm import Session

from nexusdata.core.metadata.typings import MODEL, ID
from nexusdata.utils.abstractions import AbstractRepository


class SimpleSessionRepository(AbstractRepository[MODEL, ID], ABC):

    def __init__(self, session:Session):
        super().__init__()
        self._session = session

    def save(self, entity:MODEL) -> MODEL:
        self._session.add(entity)
        self._session.flush([entity])
        return entity

    def save_all(self, entities:list[MODEL]) -> list[MODEL]:
        self._session.add_all(entities)
        self._session.flush(entities)
        return entities

    def find_by_id(self, _id:ID) -> MODEL:
        return self._session.get(self._model, _id)

    def count(self) -> int:
        return self._session.query(func.count()).select_from(self._model).scalar()

    def delete(self, entity:MODEL):
        self._session.delete(entity)

    def delete_by_id(self, _id:ID):
        e = self.find_by_id(_id)
        self._session.delete(e)