from typing import Optional

from sqlmodel import SQLModel, Field


class Role(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    name:str = Field(nullable=False, unique=True)