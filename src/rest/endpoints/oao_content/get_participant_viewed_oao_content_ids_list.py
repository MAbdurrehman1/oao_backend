from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import get_participant_viewed_oao_content_ids_list
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class GetParticipantViewedOAOContentIDsListResponseModel(BaseModel):
    result: list[int]


@router.get("/oao_content/views/", tags=[Tags.participation])
def get_participant_viewed_oao_content_ids_list_endpoint(
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> GetParticipantViewedOAOContentIDsListResponseModel:
    assert isinstance(user.id, int)
    oao_content_ids = get_participant_viewed_oao_content_ids_list(
        user_id=user.id,
    )
    return GetParticipantViewedOAOContentIDsListResponseModel(
        result=oao_content_ids,
    )
