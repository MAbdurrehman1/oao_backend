import logging
from uuid import UUID

from pydantic import BaseModel

from settings import configs
from services import login_user_with_magic_link
from ...router import router, Tags


logger = logging.getLogger(configs.app_title)


class LoginWithMagicLinkRequestModel(BaseModel):
    token: UUID


class LoginWithMagicLinkResponseModel(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/m-link/login/", tags=[Tags.auth])
def login_with_magic_link_endpoint(
    payload: LoginWithMagicLinkRequestModel,
) -> LoginWithMagicLinkResponseModel:
    tokens = login_user_with_magic_link(token=payload.token)
    return LoginWithMagicLinkResponseModel(**tokens)
