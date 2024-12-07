from typing import Self
from uuid import UUID

from fastapi import Request, Depends, Security
from pydantic import BaseModel

from entity import User, Participant, Employee, BusinessUnit
from services import get_survey_campaign_participants
from settings import ParticipationStatus
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class ParticipantResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    role_title: str
    location: str
    status: str
    business_unit: str

    @classmethod
    def from_entity(cls, participant: Participant) -> Self:
        assert isinstance(participant.id, UUID)
        assert isinstance(participant.employee, Employee)
        assert isinstance(participant.employee.user, User)
        assert isinstance(participant.survey_campaign_id, int)
        assert isinstance(participant.employee.business_unit, BusinessUnit)
        assert isinstance(participant.employee.business_unit.name, str)
        return cls(
            id=str(participant.id),
            first_name=participant.employee.user.first_name,
            last_name=participant.employee.user.last_name,
            email=participant.employee.user.email,
            role_title=participant.employee.role_title,
            location=participant.employee.location,
            status=participant.status,
            business_unit=participant.employee.business_unit.name,
        )


class GetSurveyCampaignParticipantsResponseModel(BaseModel):
    total_count: int
    result: list[ParticipantResponse]


@router.get("/survey-campaigns/{_id}/participants/", tags=[Tags.admin])
def get_survey_campaign_participants_endpoint(
    request: Request,
    _id: int,
    offset: int = 0,
    limit: int = 10,
    status: ParticipationStatus | None = None,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> GetSurveyCampaignParticipantsResponseModel:
    total_count, participants = get_survey_campaign_participants(
        campaign_id=_id,
        offset=offset,
        limit=limit,
        status=status,
    )
    return GetSurveyCampaignParticipantsResponseModel(
        total_count=total_count,
        result=[
            ParticipantResponse.from_entity(participant) for participant in participants
        ],
    )
