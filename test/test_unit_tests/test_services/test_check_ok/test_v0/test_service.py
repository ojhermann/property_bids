import httpx
import pytest
from httpx import AsyncClient
from main import app
from starlette import status
from services.check_ok.v0.check_ok import check_ok_response
from services.check_ok.v0.service import router


@pytest.mark.asyncio
async def test_check_ok():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response: httpx.Response = await ac.get(router.prefix)

    assert response.status_code == status.HTTP_200_OK

    response_dict: dict[str, str] = response.json()
    expected_dict: dict[str, str] = check_ok_response().dict()
    assert response_dict == expected_dict
