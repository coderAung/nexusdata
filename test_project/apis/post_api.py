from fastapi import APIRouter, Depends

from test_project.configs.injectables import inject_post_service
from test_project.services.post_service import PostService
from test_project.configs.security import sec

router = APIRouter(prefix="/posts")

@router.get("")
@sec.authenticated
async def index(
        service:PostService = Depends(inject_post_service),
):
    return await service.get_all()