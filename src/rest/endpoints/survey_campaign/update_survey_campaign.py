from datetime import datetime
from typing import Self

from fastapi import Request, Depends, Security
from pydantic import BaseModel

from entity import User, SurveyCampaign
from services import update_survey_campaign
from settings import configs
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class UpdateSurveyCampaignRequestModel(BaseModel):
    title: str | None = None
    start_date_str: str | None = None
    end_date_str: str | None = None


class SurveyCampaignResponse(BaseModel):
    id: int
    title: str
    start_date: str
    end_date: str
    created_at: str
    updated_at: str

    @classmethod
    def from_survey_campaign(cls, survey_campaign: SurveyCampaign) -> Self:
        assert isinstance(survey_campaign.id, int)
        assert isinstance(survey_campaign.start_date, datetime)
        assert isinstance(survey_campaign.end_date, datetime)
        assert isinstance(survey_campaign.created_at, datetime)
        assert isinstance(survey_campaign.updated_at, datetime)
        return cls(
            id=survey_campaign.id,
            title=survey_campaign.title,
            start_date=survey_campaign.start_date.strftime(configs.date_time_format),
            end_date=survey_campaign.end_date.strftime(configs.date_time_format),
            created_at=survey_campaign.created_at.strftime(configs.date_time_format),
            updated_at=survey_campaign.updated_at.strftime(configs.date_time_format),
        )


class UpdateSurveyCampaignResponseModel(BaseModel):
    result: SurveyCampaignResponse


@router.put("/survey-campaigns/{_id}/", tags=[Tags.admin])
def update_survey_campaign_endpoint(
    request: Request,
    _id: int,
    payload: UpdateSurveyCampaignRequestModel,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> UpdateSurveyCampaignResponseModel:
    updated_survey_campaign = update_survey_campaign(
        campaign_id=_id,
        title=payload.title,
        start_date_str=payload.start_date_str,
        end_date_str=payload.end_date_str,
    )
    return UpdateSurveyCampaignResponseModel(
        result=SurveyCampaignResponse.from_survey_campaign(updated_survey_campaign)
    )
