import os
from dotenv import load_dotenv

load_dotenv()

allowed_origins: dict[str, list[str]] = dict(
    development=["http://localhost:8000"],
    staging=["https://staging.url"],
    production=["https://production.url"],
)

cors_options: dict[str, list[str]] = dict(
    allow_origins=allowed_origins[os.getenv("WHICH_ENV")],
    allow_credentials=True,
    allow_methods=["GET", "DELETE", "POST"],
    allow_headers=["*"],
)
