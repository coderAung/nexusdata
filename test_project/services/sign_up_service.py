from nexusdata.asyncs.decorators import transactional
from nexusdata.orms.services import AsyncNexusService
from test_project.configs.dtos import ModificationResult, SignUpForm
from test_project.models.account import Account
from test_project.repos.account_repo import AccountRepo
from test_project.utils.exception import AppBusinessException
from test_project.utils.singletons import password_hasher


class SignUpService(AsyncNexusService):

    repo:AccountRepo

    @transactional
    async def sign_up(self, form:SignUpForm) -> ModificationResult[int]:
        account = await self.repo.find_by_email(form.email)
        if account is not None:
            raise AppBusinessException("Account already exists.")
        account = Account(
            name=form.name,
            email=form.email,
            password=password_hasher.hash(form.password),
            role_id=2,
        )
        account = await self.repo.save(account)
        return ModificationResult(id=account.id)
        