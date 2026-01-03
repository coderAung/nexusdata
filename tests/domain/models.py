from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from tests.domain.abstractions import BaseModel


class Account(BaseModel):
    __tablename__ = "account"
    _id:Mapped[int] = Column(Integer, primary_key=True)
    name:Mapped[str] = Column(String, nullable=False)
    email:Mapped[str] = Column(String, nullable=False, unique=True)
    password:Mapped[str] = Column(String, nullable=False)

class Post(BaseModel):
    __tablename__ = "post"
    _id:Mapped[int] = Column(Integer, primary_key=True)
    content:Mapped[str] = Column(String, nullable=False)
    account_id:Mapped[int] = Column(Integer, ForeignKey("account._id"), nullable=False)
    account:Mapped["Account"] = relationship("Account")