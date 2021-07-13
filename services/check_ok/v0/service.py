from http import HTTPStatus

from fastapi import APIRouter

from models.check_ok.v0.model import CheckOk
from services.check_ok.v0.check_ok import check_ok_response

CHECK_OK: str = "check_ok"

router = APIRouter(
    prefix=f"/{CHECK_OK}",
    tags=[
        CHECK_OK,
    ]
)

TAGS_METADATA: dict[str, str] = {
    "name": CHECK_OK,
}


@router.get(
    path="/",
    response_model=CheckOk,
    status_code=HTTPStatus.OK,
)
async def check_ok():
    """
    Endpoint that will return a 200 response if services are able to run.
    """
    return check_ok_response()
