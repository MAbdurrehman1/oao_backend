from fastapi import Depends
from pydantic import BaseModel

from entity import User
from services import view_oao_content
from ..dependencies import EmployeeRequired
from ...router import router, Tags


class ViewOAOContentResponseModel(BaseModel):
    result: str = "OAO Content Viewed Successfully"


@router.post(
    "/oao_content/{_id}/views/",
    tags=[Tags.participation],
)
def view_oao_content_endpoint(
    _id: int,
    user: User = Depends(EmployeeRequired()),
) -> ViewOAOContentResponseModel:
    assert isinstance(user.id, int)
    view_oao_content(
        content_id=_id,
        user_id=user.id,
    )
    return ViewOAOContentResponseModel()
