from datetime import datetime
from typing import Self

from fastapi import Request, Depends, Security
from pydantic import BaseModel

from entity import User, SurveyCampaign
from services import get_organization_survey_campaigns
from settings import configs
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class SurveyCampaignResponse(BaseModel):
    id: int
    title: str
    start_date: str
    end_date: str
    participants_count: int
    invited_participants_count: int
    responded_participants_count: int
    created_at: str
    updated_at: str

    @classmethod
    def from_survey_campaign(cls, survey_campaign: SurveyCampaign) -> Self:
        assert isinstance(survey_campaign.id, int)
        assert isinstance(survey_campaign.start_date, datetime)
        assert isinstance(survey_campaign.end_date, datetime)
        assert isinstance(survey_campaign.participants_count, int)
        assert isinstance(survey_campaign.invited_participants_count, int)
        assert isinstance(survey_campaign.responded_participants_count, int)
        assert isinstance(survey_campaign.created_at, datetime)
        assert isinstance(survey_campaign.updated_at, datetime)
        return cls(
            id=survey_campaign.id,
            title=survey_campaign.title,
            start_date=survey_campaign.start_date.strftime(configs.date_time_format),
            end_date=survey_campaign.end_date.strftime(configs.date_time_format),
            participants_count=survey_campaign.participants_count,
            invited_participants_count=survey_campaign.invited_participants_count,
            responded_participants_count=survey_campaign.responded_participants_count,
            created_at=survey_campaign.created_at.strftime(configs.date_time_format),
            updated_at=survey_campaign.updated_at.strftime(configs.date_time_format),
        )


class GetSurveyCampaignResponseModel(BaseModel):
    total_count: int
    result: list[SurveyCampaignResponse]


@router.get("/organizations/{_id}/survey-campaigns/", tags=[Tags.admin])
def get_organization_survey_campaigns_endpoint(
    request: Request,
    _id: int,
    offset: int = 0,
    limit: int = 10,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> GetSurveyCampaignResponseModel:
    total_count, survey_campaigns = get_organization_survey_campaigns(
        organization_id=_id,
        offset=offset,
        limit=limit,
    )
    return GetSurveyCampaignResponseModel(
        total_count=total_count,
        result=[
            SurveyCampaignResponse.from_survey_campaign(survey_campaign)
            for survey_campaign in survey_campaigns
        ],
    )
