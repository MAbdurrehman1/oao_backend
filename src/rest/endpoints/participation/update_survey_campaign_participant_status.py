from uuid import UUID

from fastapi import Request, Depends, Security
from pydantic import BaseModel

from entity import User
from services import update_survey_campaign_participant_status
from settings import ParticipationStatus
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class UpdateSurveyCampaignParticipantStatusRequestModel(BaseModel):
    status: ParticipationStatus


class UpdateSurveyCampaignParticipantStatusResponseModel(BaseModel):
    result: str = "Participant Status Changed successfully"


@router.put(
    "/survey-campaigns/{campaign_id}/participants/{participant_id}/",
    tags=[Tags.admin],
)
def update_survey_campaign_participant_status_endpoint(
    request: Request,
    payload: UpdateSurveyCampaignParticipantStatusRequestModel,
    campaign_id: int,
    participant_id: UUID,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> UpdateSurveyCampaignParticipantStatusResponseModel:
    update_survey_campaign_participant_status(
        campaign_id=campaign_id,
        participant_id=participant_id,
        status=payload.status,
    )
    return UpdateSurveyCampaignParticipantStatusResponseModel()
