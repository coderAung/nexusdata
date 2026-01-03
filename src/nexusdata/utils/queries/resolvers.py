from typing import Type, Callable, Any, get_args

from sqlalchemy import MappingResult, RowMapping

from nexusdata.core.metadata.typings import DTO
from nexusdata.utils.queries.utilities import is_collection, is_number, is_str, is_keyword


def resolve_cls_from_return_type(rt:Type[DTO]):
    if not is_collection(rt):
        return rt
    return get_args(rt)[0]


def resolve_dto_func_from_cls(cls:Type[DTO]) -> Callable[[RowMapping], DTO]:
    if is_number(cls): return lambda a: list(a.values())[0]
    if is_str(cls): return lambda  a: str(a)
    return lambda a: cls(**a)


def resolve_result(
        result:MappingResult,
        dto:Type[DTO] | None = None,
        map_func:Callable[[RowMapping], DTO | Any] | None = None,
        rt:Any | None = None):

    if dto is None and rt is None and map_func is None:
        return result.all()

    cls = dto if dto is not None else resolve_cls_from_return_type(rt)
    dto_func = map_func if map_func is not None else resolve_dto_func_from_cls(cls)

    if rt is None or is_collection(rt):
        return [dto_func(a) for a in result.all()]

    return dto_func(result.first())

def resolve_chain(chain:list[str]) -> list[str]:
    resolves:list[str] = []
    skip_one = False

    for i in range(len(chain)):
        if skip_one:
            skip_one = False
            continue
        current = chain[i]
        if is_keyword(current) or i == len(chain) - 1:
            resolves.append(current)
        else:
            checkpoint = chain[i + 1]
            if is_keyword(checkpoint):
                resolves.append(current)
            else:
                resolves.append(f"{current}_{checkpoint}")
                skip_one = True
    return resolves

def resolve_placeholders(chain:list[str]) -> list[str]:
    resolves = chain.copy()
    for i in range(len(resolves)):
        item = resolves[i]
        if is_keyword(item):continue
        count = 0
        for j in range(i+1, len(resolves)):
            if item != resolves[j]:continue
            if count == 0:
                count += 1
                resolves[i] = f"{item}{count}"
            count += 1
            resolves[j] = f"{item}{count}"
    return resolves

