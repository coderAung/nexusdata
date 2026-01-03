from abc import ABC
from typing import Generic, Type, get_args

from nexusdata.core.metadata.typings import MODEL, ID


class AbstractRepository(Generic[MODEL, ID], ABC):

    def __init__(self):
        self._model:Type[MODEL] = self.__class__.__resolve_model__()

    @classmethod
    def __resolve_model__(cls) -> Type[MODEL]:
        return get_args(cls.__orig_bases__[0])[0]