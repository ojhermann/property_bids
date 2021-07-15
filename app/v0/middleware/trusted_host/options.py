import os

from dotenv import load_dotenv

load_dotenv()

allowed_hosts: dict[str, list[str]] = dict(
    development=["localhost"],
    staging=["staginghost"],
    production=["productionhost"],
)

trusted_host_options: dict[str, list[str]] = dict(
    allowed_hosts=allowed_hosts[os.getenv("ALLOWED_HOST")],
)
