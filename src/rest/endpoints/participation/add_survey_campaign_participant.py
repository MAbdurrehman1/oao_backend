from fastapi import Request, Depends, Security
from pydantic import BaseModel

from entity import User
from services import add_participant_to_survey_campaign
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class AddParticipantResponse(BaseModel):
    participant_id: str


class AddSurveyCampaignParticipantResponseModel(BaseModel):
    result: AddParticipantResponse


class AddSurveyCampaignParticipantRequestModel(BaseModel):
    employee_email: str


@router.post("/survey-campaigns/{_id}/participants/", tags=[Tags.admin])
def add_survey_campaign_participant_endpoint(
    request: Request,
    payload: AddSurveyCampaignParticipantRequestModel,
    _id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> AddSurveyCampaignParticipantResponseModel:
    participant_id = add_participant_to_survey_campaign(
        campaign_id=_id,
        employee_email=payload.employee_email,
    )
    return AddSurveyCampaignParticipantResponseModel(
        result=AddParticipantResponse(participant_id=str(participant_id))
    )
