from dataclasses import dataclass

from nexusdata.core.metadata.typings import MODEL
from nexusdata.legacy.decorators import query, transactional
from nexusdata.orms.repositories import NexusRepository, AsyncNexusRepository
from tests.domain.models import Account, Post


@dataclass
class AccountDto:
    _id:int
    name:str

class AccountRepo(NexusRepository[Account, int]):

    @transactional(read_only=False)
    def save_all(self, entities: list[MODEL]) -> list[MODEL]:
        return super().save_all(entities)

    @query
    def find_by_name_like(self, name:str) -> list[Account]:
        pass

    @query
    def find_by_email_like(self, email:str) -> list[Account]:
        pass

    @query(sql="select _id, name from account", dto=AccountDto)
    def get_dtos_by_name(self, name:str) -> list[AccountDto]:
        pass

class AsyncAccountRepo(AsyncNexusRepository[Account, int]):pass

class PostRepo(AsyncNexusRepository[Post, int]):pass