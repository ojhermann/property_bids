from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.v0.middleware.cors.options import cors_options
from app.v0.middleware.trusted_host.options import trusted_host_options
from services.active import *

tags_metadata: list[dict[str, str]] = [
    CHECK_OK,
]


class PropertyBids(FastAPI):
    def __init__(self, **extra: Any):
        super().__init__(
            title="Property Bids",
            openapi_tags=tags_metadata,
            **extra
        )
        self.set_middleware()
        self.set_routers()

    def set_middleware(self):
        self.add_middleware(
            TrustedHostMiddleware,
            **trusted_host_options,
        )
        self.add_middleware(
            CORSMiddleware,
            **cors_options,
        )

    def set_routers(self):
        self.include_router(check_ok)
