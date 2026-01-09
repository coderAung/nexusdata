
from nexusdata.orms.services import AsyncNexusService
from test_project.configs.dtos import AccountInfo, AuthenticationResult, SignInForm
from test_project.repos.account_repo import AccountRepo
from test_project.utils.jwts import create_access_token
from test_project.utils.singletons import password_hasher


class SignInService(AsyncNexusService):

    repo:AccountRepo

    async def sign_in(self, form:SignInForm) -> AuthenticationResult:
        account = await self.repo.find_by_email(form.email)
        if account is None:
            raise ValueError("Account not found.")

        print("===========================")
        print(account)
        print("===========================")

        if not password_hasher.verify(form.password, account.password):
            raise ValueError("Wrong Password.")

        info = AccountInfo(
            id=account.id,
            name=account.name,
            email=account.email,
            role=account.role.name,
        )
        return AuthenticationResult(
            access_token=create_access_token(info.model_dump()),
            account_info=info,
        )