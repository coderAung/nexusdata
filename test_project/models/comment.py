from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Comment(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True)
    content:str = Field(nullable=False)
    post_id:int = Field(nullable=False, foreign_key="post.id")
    account_id:int = Field(nullable=False, foreign_key="account.id")
    post:"Post" = Relationship(back_populates="comments")