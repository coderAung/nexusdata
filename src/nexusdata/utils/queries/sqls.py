from typing import Callable, Type

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

sql_logics:dict[str, str] = {
    "ne": "<>",
    "eq": "=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    "like": "like",
}