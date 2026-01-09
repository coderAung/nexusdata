from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Post(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    content:str = Field(nullable=False)
    account_id:int = Field(nullable=False, foreign_key="account.id")
    account:"Account" = Relationship()
    comments:list["Comment"] = Relationship(back_populates="post")