from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase

MODEL = TypeVar("MODEL", bound=DeclarativeBase)
ID = TypeVar("ID")
DTO = TypeVar("DTO")
R = TypeVar("R")
U = TypeVar("U")
E = TypeVar("E")
RT = TypeVar("RT")