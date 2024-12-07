import logging

from pydantic import BaseModel

from services import refreshing_token
from settings import configs
from ...router import router, Tags


logger = logging.getLogger(configs.app_title)


class RefreshTokenRequestModel(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenResponseModel(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/auth/refresh_token/", tags=[Tags.auth])
def refresh_token_endpoint(
    payload: RefreshTokenRequestModel,
) -> RefreshTokenResponseModel:
    tokens = refreshing_token(
        access_token=payload.access_token, refresh_token=payload.refresh_token
    )
    return RefreshTokenResponseModel(**tokens)
