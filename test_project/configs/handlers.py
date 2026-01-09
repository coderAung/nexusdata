from http import HTTPStatus

from starlette.requests import Request
from starlette.responses import JSONResponse

from test_project.utils.exception import AppBusinessException


def handle(request:Request, e:AppBusinessException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=e.msg,
    )