import warnings
from typing import Any, Callable, Type

from nexusdata.core.metadata.typings import MODEL
from nexusdata.core.queries.generators import NexusQueryGenerator
from nexusdata.core.queries.specials import NexusQuery
from nexusdata.utils.exceptions import NexusQueryException
from nexusdata.utils.queries.resolvers import resolve_chain, resolve_placeholders
from nexusdata.utils.queries.sqls import sql_queries, sql_logics, sql_model_queries
from nexusdata.utils.queries.utilities import is_logics, is_keyword


class NexusQueryGeneratorImpl(NexusQueryGenerator):

    def generate_query(self, fn: Callable[..., Any] | Any, model: Type[MODEL], *args, **kwargs) -> NexusQuery:
        fn_name:str = fn.__name__
        [sql_key, criteria] = fn_name.split("_by_")

        if not sql_queries.keys().__contains__(sql_key):
            raise NexusQueryException("Invalid naming conventions.")

        chain = resolve_chain(criteria.split("_"))
        placeholders = resolve_placeholders(chain)

        where = self.generate_where(chain, placeholders)

        query = sql_model_queries.get(sql_key)(model)
        params = self.generate_params(placeholders, *args, **kwargs)

        return NexusQuery(key=sql_key, query=query, where=where, params=params)

    def generate_where(self, chain: list[str], placeholders: list[str]) -> str:

        where = ""
        is_next = False

        for i in range(len(chain)):
            op = "="
            c = chain[i]

            if is_logics(c): continue
            if is_keyword(c):
                where += f" {c}"
                is_next = False
                continue

            if is_next:
                warnings.warn("Missing 'and', 'or'.")

            if i != len(chain) - 1:
                sub = chain[i + 1]
                op = sql_logics.get(sub) if sql_logics.get(sub) is not None else op

            where += f" {c} {op} :{placeholders[i]}"

            if i != len(chain) - 1:
                is_next = True
        return where

    def generate_params(self, placeholders: list[str], *args, **kwargs) -> dict[str, Any]:
        params: dict[str, Any] = {}
        placeholders = [p for p in placeholders if not is_keyword(p)]
        if len(params) != len(args) and len(params) != len(kwargs):
            raise NexusQueryException("Sql parameters are not match.")

        if len(args) != 0:
            for i in range(len(args)):
                params[placeholders[i]] = args[i]
        elif len(kwargs) != 0:
            for p in placeholders:
                params[p] = kwargs.get(p)
        return params