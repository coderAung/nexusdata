from http import HTTPStatus

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.requests import Request

from nexusdata.security.specials import NexusSecurity
from test_project.configs.database import get_async_session
from test_project.models.account import Account
from test_project.models.role import Role
from test_project.utils.exception import AppBusinessException
from test_project.utils.jwts import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def current_user(
        request:Request,
        token:str = Depends(oauth2_scheme),
        session:AsyncSession = Depends(get_async_session)) -> Account:
    try:
        payload = decode_access_token(token)
    except InvalidSignatureError:
        raise AppBusinessException("Invalid token.")
    email:str = payload.get("email")
    account:Account = (await session.execute(select(Account).where(Account.email == email))).scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    request.state.user = account
    return account

sec = NexusSecurity(
    user_cls=Account,
    user_supplier=lambda: Depends(current_user),
    role_cls=Role,
    role_func=lambda u: u.role.name,
    exception=HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
    )
)