import re
from uuid import UUID

import pytest

from cexceptions import UniqueException, NotFoundException
from entity import BusinessUnit
from .helpers import (
    create_some_organization,
    create_some_file,
    create_some_employee,
    create_some_employee_survey_campaign,
    create_some_business_unit,
)
from ..business_unit_repository import BusinessUnitRepository


def _assert_business_units_equal(bu1, bu2):
    assert bu1.name == bu2.name
    assert bu1.parent_id == bu2.parent_id
    assert bu1.organization_id == bu2.organization_id
    assert bu1.id == bu2.id


def test_get_business_unit_by_id_when_does_not_exist():
    with pytest.raises(
        NotFoundException, match=re.escape("BusinessUnit with ID (1) not found.")
    ):
        BusinessUnitRepository.get_by_id(1)


def test_successful_store(cleanup_database, cleanup_media):
    organization = create_some_organization()
    bu = BusinessUnit(organization=organization, name="Test", parent_id=None)
    result_bu = BusinessUnitRepository.store(bu)
    assert isinstance(result_bu.id, int)
    retrieved_bu = BusinessUnitRepository.get_by_id(result_bu.id)
    _assert_business_units_equal(result_bu, retrieved_bu)


def test_get_sub_units_with_participation(cleanup_database, cleanup_media):
    file = create_some_file()
    organization = create_some_organization(logo_id=file.id)
    assert isinstance(organization.id, int)
    bu1 = create_some_business_unit(
        organization_id=organization.id, name="Origin", parent_id=None
    )
    bu2 = create_some_business_unit(
        organization_id=organization.id, name="Sub1", parent_id=bu1.id
    )
    bu3 = create_some_business_unit(
        organization_id=organization.id, name="Sub2", parent_id=bu1.id
    )
    bu4 = create_some_business_unit(
        organization_id=organization.id, name="Sub1-Sub1", parent_id=bu2.id
    )
    bu5 = create_some_business_unit(
        organization_id=organization.id, name="Sub1-Sub2", parent_id=bu2.id
    )
    bu6 = create_some_business_unit(
        organization_id=organization.id, name="Sub2-Sub1", parent_id=bu3.id
    )
    e1 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu2.id,
        email="test1@example.com",
    )
    e2 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu3.id,
        email="test2@example.com",
    )
    e3 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu3.id,
        email="test3@example.com",
    )
    e4 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu4.id,
        email="test4@example.com",
    )
    e5 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu5.id,
        email="test5@example.com",
    )
    e6 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu6.id,
        email="test6@example.com",
    )
    e7 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu6.id,
        email="test7@example.com",
    )
    e8 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu6.id,
        email="test8@example.com",
    )
    e9 = create_some_employee(
        organization_id=organization.id,
        business_unit_id=bu6.id,
        email="test9@example.com",
    )
    create_some_employee_survey_campaign(
        organization_id=organization.id,
        participant_ids=[e1.id, e2.id, e3.id, e4.id, e5.id, e6.id, e7.id, e8.id, e9.id],
    )
    result = BusinessUnitRepository.get_sub_units_with_participation(
        business_unit_ids=[bu2.id, bu3.id],  # type: ignore
    )
    assert len(result) == 9
    assert isinstance(result[0][0], int)
    assert isinstance(result[0][1], UUID)


def test_duplicate_business_unit(cleanup_database, cleanup_media):
    organization = create_some_organization()
    bu = BusinessUnit(organization=organization, name="Test", parent_id=None)
    stored_bu = BusinessUnitRepository.store(bu)
    bu1 = BusinessUnit(organization=organization, name="Test", parent_id=stored_bu.id)
    BusinessUnitRepository.store(bu1)
    with pytest.raises(
        UniqueException,
        match=re.escape(
            f"name-organization_id-parent_id"
            f" ({bu1.name}-{bu1.organization_id}-{bu1.parent_id})"
            f" already exists."
        ),
    ):
        BusinessUnitRepository.store(bu1)


def test_get_missing_ids(cleanup_database, cleanup_media):
    organization = create_some_organization()
    bu = BusinessUnit(organization=organization, name="Test", parent_id=None)
    retrieved_bu = BusinessUnitRepository.store(bu)
    assert isinstance(organization.id, int)
    assert isinstance(retrieved_bu.id, int)
    retrieved_list = BusinessUnitRepository.get_missing_business_unit_ids(
        organization_id=organization.id,
        _ids=[retrieved_bu.id, 1.1, 1.2],  # type: ignore
    )
    assert set(retrieved_list) == {1.1, 1.2}
