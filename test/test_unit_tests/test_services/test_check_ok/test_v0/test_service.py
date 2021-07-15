import os

import httpx
import pytest

from httpx import AsyncClient
from starlette import status

from app.v0.property_bids import PropertyBids
from app.v0.middleware.trusted_host.options import allowed_hosts, bogus_test_host
from services.check_ok.v0.check_ok import check_ok_response
from services.check_ok.v0.service import router


@pytest.mark.asyncio
async def test_check_ok():
    app: PropertyBids = PropertyBids()
    allowed_host: str = allowed_hosts[os.getenv("ALLOWED_HOST")][0]
    root: str = "http://" if allowed_host == "development" else "https://"
    base_url: str = f"{root}{allowed_host}"

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response: httpx.Response = await ac.get(router.prefix)

    assert response.status_code == status.HTTP_200_OK

    response_dict: dict[str, str] = response.json()
    expected_dict: dict[str, str] = check_ok_response().dict()
    assert response_dict == expected_dict


@pytest.mark.asyncio
async def test_check_ok_only_works_on_allowed_host():
    app: PropertyBids = PropertyBids()
    root: str = "http://" if allowed_hosts[os.getenv("ALLOWED_HOST")][0] == "development" else "https://"
    bogus_url: str = f"{root}{bogus_test_host}"

    async with AsyncClient(app=app, base_url=bogus_url) as ac:
        response: httpx.Response = await ac.get(router.prefix)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
