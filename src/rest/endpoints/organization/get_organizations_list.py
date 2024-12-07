from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, Organization, File
from services import get_organizations
from settings import configs
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class OrganizationResponse(BaseModel):
    id: int
    company_name: str
    industry: str
    hq_location: str
    size: str
    logo_url: str
    meta_data: dict | None
    created_at: str
    updated_at: str

    @classmethod
    def from_organization(cls, organization: Organization) -> Self:
        assert isinstance(organization.id, int), "organization ID must not be null"
        assert isinstance(
            organization.created_at, datetime
        ), "organization created_at must not be null"
        assert isinstance(
            organization.updated_at, datetime
        ), "organization updated_at must not be null"
        assert isinstance(organization.logo, File)
        assert isinstance(organization.logo.file_path, str)
        return cls(
            id=organization.id,
            company_name=organization.company_name,
            industry=organization.industry,
            hq_location=organization.hq_location,
            size=organization.size,
            logo_url=organization.logo.file_url,
            meta_data=organization.meta_data,
            created_at=organization.created_at.strftime(configs.date_time_format),
            updated_at=organization.updated_at.strftime(configs.date_time_format),
        )


class GetOrganizationsResponseModel(BaseModel):
    total_count: int
    result: list[OrganizationResponse]


@router.get("/organizations/", tags=[Tags.admin])
def get_organizations_list_endpoint(
    offset: int = 0,
    limit: int = 5,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    total_count, organizations = get_organizations(offset=offset, limit=limit)
    response_models = [
        OrganizationResponse.from_organization(org) for org in organizations
    ]
    return GetOrganizationsResponseModel(
        result=response_models,
        total_count=total_count,
    )
