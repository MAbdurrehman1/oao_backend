import logging

from pydantic import BaseModel

from services import login_user
from settings import configs
from ...router import router, Tags


logger = logging.getLogger(configs.app_title)


class UserLoginRequestModel(BaseModel):
    email: str
    password: str


class UserLoginResponseModel(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/auth/login/", tags=[Tags.auth])
def user_login_endpoint(payload: UserLoginRequestModel) -> UserLoginResponseModel:
    tokens = login_user(email=payload.email, password=payload.password)
    return UserLoginResponseModel(**tokens)
