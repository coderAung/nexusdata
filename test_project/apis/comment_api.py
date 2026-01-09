from fastapi import APIRouter, Depends, Request

from test_project.configs.dtos import CommentForm
from test_project.configs.injectables import inject_comment_service
from test_project.configs.security import sec
from test_project.services.comment_service import CommentService

router = APIRouter(prefix="/comments")

@router.get("")
@sec.authenticated(authorized_roles=["member"])
async def index(service:CommentService = Depends(inject_comment_service)):
    return await service.get_all()

@router.post("")
@sec.authenticated(authorized_roles=["member"])
async def save(
        request:Request,
        form:CommentForm,
        service:CommentService = Depends(inject_comment_service),
):
    return await service.save(form, request.state.user.id)

@router.delete("/{_id}")
@sec.authenticated(authorized_roles=["member"])
async def save(
        _id:int,
        service:CommentService = Depends(inject_comment_service),
):
    try:
        await service.delete_by_id(_id)
        return True
    except Exception as e:
        print(e)
        return False