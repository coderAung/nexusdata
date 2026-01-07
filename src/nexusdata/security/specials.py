import inspect
from dataclasses import dataclass
from functools import wraps
from inspect import Parameter
from typing import Callable, Any, Generic, Type

from nexusdata.core.metadata.typings import R, U, E
from nexusdata.utils.exceptions import NexusSecurityException


@dataclass(frozen=True)
class NexusSecurity(Generic[U, R, E]):
    user_cls:Type[U]
    role_cls:Type[R]
    user_supplier:Callable[[], U]
    role_func:Callable[[U], R]
    exception:E = NexusSecurityException("Forbidden access.")

    AUTHENTICATED_USER = "authenticated_user"

    def authenticated(self, func:Callable[..., Any] | None = None, *, authorized_roles:list[R] = None):
        def decorator(fn:Callable[..., Any]):
            sig = inspect.signature(fn)
            user_param = Parameter(
                self.AUTHENTICATED_USER,
                kind=Parameter.KEYWORD_ONLY,
                annotation=self.user_cls,
                default=self.user_supplier()
            )
            new_sig = sig.replace(
                parameters=[*sig.parameters.values(), user_param]
            )

            @wraps(fn)
            def wrapper(*args, **kwargs):
                if kwargs.__contains__(self.AUTHENTICATED_USER):
                    user:U = kwargs.get(self.AUTHENTICATED_USER)
                    kwargs.pop(self.AUTHENTICATED_USER)
                else:
                    user:U = self.user_supplier()
                if user is None:
                    raise NexusSecurityException("Authenticated is not found.")

                if authorized_roles and self.role_func(user) not in authorized_roles:
                    raise self.exception
                return fn(*args, **kwargs)

            wrapper.__signature__ = new_sig
            return wrapper

        if func is None:
            return decorator
        return decorator(fn=func)
