from fastapi import APIRouter, Depends

from test_project.configs.dtos import SignUpForm
from test_project.configs.injectables import inject_sign_up_service
from test_project.services.sign_up_service import SignUpService

router = APIRouter(prefix="/sign-up")

@router.post("")
async def sign_up(
        form:SignUpForm,
        service:SignUpService = Depends(inject_sign_up_service)
):
    return await service.sign_up(form)