import os

from dotenv import load_dotenv

load_dotenv()

bogus_test_host: str = "bogus_test_host"

allowed_hosts: dict[str, list[str]] = dict(
    development=["localhost"],
    staging=["staginghost"],
    production=["productionhost"],
)

trusted_host_options: dict[str, list[str]] = dict(
    allowed_hosts=allowed_hosts[os.getenv("ALLOWED_HOST")],
)
