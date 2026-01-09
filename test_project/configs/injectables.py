from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from test_project.configs.database import get_async_session
from test_project.services.comment_service import CommentService
from test_project.services.post_service import PostService
from test_project.services.sign_in_service import SignInService
from test_project.services.sign_up_service import SignUpService


def inject_post_service(session:AsyncSession = Depends(get_async_session)) -> PostService:
    return PostService(session=session)

def inject_comment_service(session:AsyncSession = Depends(get_async_session)) -> CommentService:
    return CommentService(session=session)

def inject_sign_in_service(session:AsyncSession = Depends(get_async_session)) -> SignInService:
    return SignInService(session=session)

def inject_sign_up_service(session:AsyncSession = Depends(get_async_session)) -> SignUpService:
    return SignUpService(session=session)