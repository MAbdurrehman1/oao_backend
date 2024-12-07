from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import get_modules_urls
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class UrlResponse(BaseModel):
    order: int
    url: str


class GetModulesURLsResponseModel(BaseModel):
    passed_order: int
    result: list[UrlResponse]


@router.get("/modules/urls/", tags=[Tags.participation])
def get_modules_urls_endpoint(
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> GetModulesURLsResponseModel:
    assert isinstance(user.id, int)
    passed_order, url_data = get_modules_urls(
        user_id=user.id,
    )
    url_response = [UrlResponse(order=k, url=v) for k, v in url_data.items()]
    return GetModulesURLsResponseModel(result=url_response, passed_order=passed_order)
