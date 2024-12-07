from fastapi import UploadFile, Request, Depends, Security
from pydantic import BaseModel

from entity import User
from services import submit_survey_campaign
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class CreateSurveyCampaignResponseModel(BaseModel):
    result: str = "Survey Campaign Created Successfully"


@router.post("/survey-campaigns/", tags=[Tags.admin])
def create_survey_campaign_endpoint(
    request: Request,
    file: UploadFile,
    title: str,
    organization_id: int,
    start_date_str: str,
    end_date_str: str,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> CreateSurveyCampaignResponseModel:
    submit_survey_campaign(
        emails_csv_file=file.file,
        title=title,
        organization_id=organization_id,
        start_date_str=start_date_str,
        end_date_str=end_date_str,
    )
    return CreateSurveyCampaignResponseModel()
