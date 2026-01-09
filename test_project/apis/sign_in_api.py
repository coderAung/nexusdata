from fastapi import APIRouter, Depends

from test_project.configs.dtos import SignInForm
from test_project.configs.injectables import inject_sign_in_service
from test_project.services.sign_in_service import SignInService

router = APIRouter(prefix="/sign-in")

@router.post("")
async def sign_in(
    form:SignInForm,
    service:SignInService = Depends(inject_sign_in_service)):
    return await service.sign_in(form)