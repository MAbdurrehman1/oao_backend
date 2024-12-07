import logging

from pydantic import BaseModel

from settings import configs
from services import send_magic_link
from ...router import router, Tags


logger = logging.getLogger(configs.app_title)


class SendMagicLinkRequestModel(BaseModel):
    email: str


class SendMagicLinkResponseModel(BaseModel):
    result: str = "Magic Link sent Successfully"


@router.post("/m-link/", tags=[Tags.auth])
def send_magic_link_endpoint(
    payload: SendMagicLinkRequestModel,
) -> SendMagicLinkResponseModel:
    send_magic_link(email=payload.email)
    return SendMagicLinkResponseModel()
