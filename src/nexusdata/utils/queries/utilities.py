from typing import Type, get_origin, Collection

from nexusdata.utils.queries.sqls import sql_logics


def is_collection(cls: Type | None) -> bool:
    try:
        return False if cls is None else issubclass(get_origin(cls), Collection)
    except Exception as e:
        print(e)
    return False

def is_number(cls:Type):
    return cls == int or cls == float

def is_str(cls:Type):
    return cls == str

def is_conjunction(item:str) -> bool:
    return item == "and" or item == "or"

def is_logics(item:str) -> bool:
    return sql_logics.__contains__(item)

def is_keyword(item:str) -> bool:
    return is_logics(item) or is_conjunction(item)