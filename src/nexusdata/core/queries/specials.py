from typing import Any

from sqlalchemy import Delete, Select


class NexusQuery:

    def __init__(self, key:str, query:Select | Delete, where:str, params:dict[str, Any]):
        self.key = key
        self.query = query
        self.where = where
        self.params = params

    @property
    def is_count(self) -> bool:
        return self.key == "count"

    @property
    def is_delete(self) -> bool:
        return self.key == "delete"

    @property
    def is_select(self) -> bool:
        return self.key == "find" or self.key == "get"
