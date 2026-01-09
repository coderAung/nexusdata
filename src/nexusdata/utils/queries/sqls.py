from typing import Callable, Type

from sqlalchemy import ClauseElement, Delete, Select, delete, func, select

from nexusdata.core.metadata.typings import MODEL


def resolve_table_name(model:Type[MODEL]):
    try:
        return model.__tablename__
    except Exception as e:
        print(e)
        return model.__name__.lower()


sql_queries:dict[str, Callable[[Type], str]] = {
    "get": lambda cls: f"select * from {resolve_table_name(cls)}",
    "find": lambda cls: f"select * from {resolve_table_name(cls)}",
    "delete": lambda cls: f"delete from {resolve_table_name(cls)}",
    "count": lambda cls: f"select count(*) as c from {resolve_table_name(cls)}",
}

sql_model_queries:dict[str, Callable[[Type[MODEL]], Select | Delete]] = {
    "get": lambda cls: select(cls),
    "find": lambda cls: select(cls),
    "delete": lambda cls: delete(cls),
    "count": lambda cls: select(func.count()).select_from(cls),
}

sql_logics:dict[str, str] = {
    "ne": "<>",
    "eq": "=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    "like": "like",
}