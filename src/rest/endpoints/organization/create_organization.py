from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import create_organization
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class CreateOrganizationRequestModel(BaseModel):
    company_name: str
    hq_location: str
    size: str
    industry: str
    meta_data: dict
    logo_id: int


class CreateOrganizationResponseModel(BaseModel):
    result: str = "organization created successfully"


@router.post("/organizations/", tags=[Tags.admin])
def create_organization_endpoint(
    payload: CreateOrganizationRequestModel,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> CreateOrganizationResponseModel:
    create_organization(
        company_name=payload.company_name,
        hq_location=payload.hq_location,
        size=payload.size,
        industry=payload.industry,
        meta_data=payload.meta_data,
        logo_id=payload.logo_id,
    )
    return CreateOrganizationResponseModel()
