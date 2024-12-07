from uuid import UUID

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import get_report_responded_participant_ids
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class GetReportParticipantIDsResponseModel(BaseModel):
    result: list[UUID]


@router.get("/management-position/{_id}/report-participants/", tags=[Tags.admin])
def get_report_responded_participant_ids_endpoint(
    _id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    participant_ids = get_report_responded_participant_ids(position_id=_id)
    return GetReportParticipantIDsResponseModel(result=participant_ids)
