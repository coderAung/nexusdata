from nexusdata.asyncs.decorators import query
from nexusdata.orms.repositories import AsyncNexusRepository
from test_project.models.account import Account


class AccountRepo(AsyncNexusRepository[Account, int]):

    @query
    async def find_by_email(self, email:str) -> Account:pass