from http import HTTPStatus

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.exceptions import HTTPException

from nexusdata.security.specials import NexusSecurity
from test_project.configs.database import get_async_session
from test_project.models.account import Account
from test_project.models.role import Role
from test_project.utils.jwts import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def current_user(token:str = Depends(oauth2_scheme), session:AsyncSession = Depends(get_async_session)) -> Account:
    payload = decode_access_token(token)
    email:str = payload.get("sub")
    account:Account = (await session.exec(select(Account).where(Account.email == email))).one_or_none()
    if account is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    return account

sec = NexusSecurity(
    user_cls=Account,
    user_supplier=lambda: Depends(current_user),
    role_cls=Role,
    role_func=lambda u: u.role,
)