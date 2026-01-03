from abc import ABC, abstractmethod
from typing import Any, Callable, Type

from nexusdata.core.queries.specials import NexusQuery


class NexusQueryGenerator(ABC):

    @abstractmethod
    def generate_query(self, fn:Callable[..., Any] | Any, model:Type, *args, **kwargs) -> NexusQuery:pass

    @abstractmethod
    def generate_where(self, chain:list[str], placeholders:list[str]) -> str:pass

    @abstractmethod
    def generate_params(self, placeholders:list[str], *args, **kwargs) -> dict[str, Any]:pass