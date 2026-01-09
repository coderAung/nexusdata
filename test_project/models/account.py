from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Account(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    email:str = Field(nullable=False, unique=True)
    name:str = Field(nullable=False, unique=True)
    password:str = Field(nullable=False, unique=True)
    role_id:int = Field(foreign_key="role.id")
    role:"Role" = Relationship(sa_relationship_kwargs={"lazy": "joined"})