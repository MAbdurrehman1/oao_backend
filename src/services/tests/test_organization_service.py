from datetime import datetime
import re

import pytest

from cexceptions import ValidationException
from entity import Organization
from repository import OrganizationRepository
from repository.tests.helpers import create_some_organization, create_some_file
from ..organization_service import create_organization, get_organizations


def test_store(cleanup_database, cleanup_media):
    logo = create_some_file()
    organization = Organization(
        company_name="Test Company Name",
        industry="Test Industry",
        hq_location="Test HQ Location",
        size="50-100",
        meta_data=dict(test_key="test_value"),
        logo_id=logo.id,
    )
    assert isinstance(logo.id, int)
    stored_organization = create_organization(
        company_name=organization.company_name,
        industry=organization.industry,
        hq_location=organization.hq_location,
        size=organization.size,
        meta_data=organization.meta_data,  # type: ignore
        logo_id=logo.id,
    )
    assert isinstance(stored_organization.id, int)
    assert isinstance(stored_organization.created_at, datetime)
    assert isinstance(stored_organization.updated_at, datetime)

    retrieved_organization = OrganizationRepository.get_by_id(stored_organization.id)
    assert retrieved_organization.equal_value(
        stored_organization
    ) and stored_organization.equal_value(organization)


def test_store_with_invalid_size(cleanup_media, cleanup_database):
    with pytest.raises(
        ValidationException,
        match=re.escape("(Invalid Size) is/are not valid value for Size."),
    ):
        logo = create_some_file()
        assert isinstance(logo.id, int)
        create_organization(
            company_name="Test Company Name",
            industry="Test Industry",
            hq_location="Test HQ Location",
            size="Invalid Size",
            meta_data={},
            logo_id=logo.id,
        )


def test_get_organizations(cleanup_database, cleanup_media):
    organizations = [
        create_some_organization(
            company_name=f"test{i+1}",
            logo_user_email=f"test{i}@example.com",
            logo_name=f"test_{i}.png",
        )
        for i in range(10)
    ]
    organization_names = {org.company_name for org in organizations}
    total_count, organization_list = get_organizations(limit=20, offset=0)
    assert total_count == 10
    assert len(organization_list) == len(organizations)
    assert set(organization_names) == {org.company_name for org in organization_list}


def test_get_organization_with_50_plus_limit(cleanup_database, cleanup_media):
    [
        create_some_organization(
            company_name=f"test{i+1}",
            logo_user_email=f"test{i}@example.com",
            logo_name=f"test_{i}.png",
        )
        for i in range(100)
    ]
    total_count, organization_list = get_organizations(limit=200, offset=0)
    assert len(organization_list) == 50
    assert total_count == 100
