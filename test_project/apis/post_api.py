from fastapi import APIRouter, Depends
from starlette.requests import Request

from test_project.configs.dtos import ModificationResult, PostForm
from test_project.configs.injectables import inject_post_service
from test_project.services.post_service import PostService
from test_project.configs.security import sec

router = APIRouter(prefix="/posts")

@router.get("")
@sec.authenticated(authorized_roles=["member"])
async def index(
        service:PostService = Depends(inject_post_service),
):
    return await service.get_all()

@router.post("", response_model=ModificationResult[int])
@sec.authenticated(authorized_roles=["member"])
async def save(
        request:Request,
        form:PostForm,
        service:PostService = Depends(inject_post_service)
):
    return await service.save(form, request.state.user.id)

@router.delete("/{_id}")
@sec.authenticated(authorized_roles=["member"])
async def delete(_id:int, service:PostService = Depends(inject_post_service)):
    try:
        await service.delete_by_id(_id)
        return True
    except Exception as e:
        print(e)
        return False