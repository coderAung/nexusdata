import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tests.domain.abstractions import BaseModel

engine = create_engine(url="sqlite:///./test.db", echo=True)

def init_db():
    BaseModel.metadata.create_all(engine)

def get_session():
    with sessionmaker(bind=engine)() as session:
        try:
            yield session
        except Exception as e:
            raise e
        finally:
            session.close()
