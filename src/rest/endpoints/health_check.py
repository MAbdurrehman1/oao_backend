import logging

from pydantic import BaseModel
from starlette.requests import Request

from settings import configs
from ..router import router, Tags


logger = logging.getLogger(configs.app_title)


class HealthCheckResponseModel(BaseModel):
    result: str = "Application is up and running"


@router.get("/health_check/", tags=[Tags.general])
def health_check(request: Request) -> HealthCheckResponseModel:
    return HealthCheckResponseModel()
