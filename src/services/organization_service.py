import re

from cexceptions import ValidationException, NotFoundException
from entity import Organization
from repository import OrganizationRepository, FileRepository


def _validate_company_size(size: str):
    if not re.match(r"\d+-\d+", size):
        raise ValidationException(entities="Size", values=size)


def create_organization(
    company_name: str,
    industry: str,
    hq_location: str,
    size: str,
    meta_data: dict,
    logo_id: int,
) -> Organization:
    _validate_company_size(size)
    if not FileRepository.exists(_id=logo_id):
        raise NotFoundException(
            entity="File",
            arg="ID",
            value=str(logo_id),
        )
    organization = Organization(
        company_name=company_name,
        industry=industry,
        hq_location=hq_location,
        size=size,
        meta_data=meta_data,
        logo_id=logo_id,
    )
    organization = OrganizationRepository.store(organization=organization)
    return organization


def get_organizations(offset: int, limit: int) -> tuple[int, list[Organization]]:
    limit = 50 if limit > 50 else limit
    total_count, organizations = OrganizationRepository.get_list(offset, limit=limit)
    return total_count, organizations
