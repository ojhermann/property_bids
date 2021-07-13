from fastapi import FastAPI

from services.active import *

tags_metadata: list[dict[str, str]] = [
    CHECK_OK,
]

app: FastAPI = FastAPI(
    title="Property Bids",
    openapi_tags=tags_metadata,
)

app.include_router(check_ok)
