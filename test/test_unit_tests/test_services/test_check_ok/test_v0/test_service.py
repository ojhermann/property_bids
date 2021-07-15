import os

import httpx
import pytest
from httpx import AsyncClient
from starlette import status

from app.v0.middleware.trusted_host.options import allowed_hosts
from app.v0.property_bids import PropertyBids
from services.check_ok.v0.check_ok import check_ok_response
from services.check_ok.v0.service import router


@pytest.mark.asyncio
async def test_it_works_as_expected():
    app: PropertyBids = PropertyBids()
    allowed_host: str = allowed_hosts[os.getenv("ALLOWED_HOST")][0]
    base_url: str = f"https://{allowed_host}"

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response: httpx.Response = await ac.get(router.prefix)

    assert response.status_code == status.HTTP_200_OK

    response_dict: dict[str, str] = response.json()
    expected_dict: dict[str, str] = check_ok_response().dict()
    assert response_dict == expected_dict
