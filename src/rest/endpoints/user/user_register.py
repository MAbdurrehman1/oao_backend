import logging

from fastapi import Depends
from pydantic import BaseModel

from entity import User
from settings import configs
from services import create_user
from ..dependencies import AdminRequired
from ...router import router, Tags


logger = logging.getLogger(configs.app_title)


class UserRegisterRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserRegisterResponseModel(BaseModel):
    result: str = "User registered successfully"


@router.post("/user/register/", tags=[Tags.accounts])
def user_register_endpoint(
    payload: UserRegisterRequestModel,
    _: User = Depends(AdminRequired()),
) -> UserRegisterResponseModel:
    create_user(payload.first_name, payload.last_name, payload.email, payload.password)
    return UserRegisterResponseModel()
