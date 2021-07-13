from pydantic import BaseModel, Field
from starlette import status


class CheckOk(BaseModel):
    """
    An object returned indicating the service is working
    """

    class Config:
        validate_assignment = True

    version: int = Field(
        default=0,
        description="Version being checked",
        allow_mutation=False,
    )

    status: int = Field(
        default=status.HTTP_200_OK,
        description="HTTP status",
        allow_mutation=False,
    )
