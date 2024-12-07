import re
from io import BytesIO

import pytest

from cexceptions import (
    NotFoundException,
    EntityProcessException,
    MissingValuesException,
    ValidationException,
)
from repository.tests.helpers import create_some_organization, create_some_business_unit
from services import import_contact_list
from .helpers import get_contacts_list_with_one_row_csv_bytes, tribble


def test_import_contact_list_with_no_organization(cleanup_database):
    with pytest.raises(
        NotFoundException, match=re.escape("Organization with ID (100) not found.")
    ):
        import_contact_list(
            organization_id=100,
            contacts_csv_file=get_contacts_list_with_one_row_csv_bytes(
                business_units_id=1,
            ),
        )


def test_import_contact_list_with_invalid_file(cleanup_database, cleanup_media):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    with pytest.raises(
        EntityProcessException,
        match=re.escape("Failed to process CSV File. please provide a valid CSV File"),
    ):
        import_contact_list(
            organization_id=organization.id,
            contacts_csv_file=BytesIO("InvalidßContent".encode("latin1")),
        )


def test_import_contacts_list_with_invalid_columns(cleanup_database, cleanup_media):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    required_columns = [
        "first_name",
        "last_name",
        "email",
        "role_title",
        "location",
        "business_unit",
    ]
    for col in required_columns:
        df = tribble(
            columns=list(set(required_columns) - {col}),
        )
        with pytest.raises(
            MissingValuesException,
            match=re.escape(f"('{col}',) is/are missing in Contacts List."),
        ):
            import_contact_list(
                organization_id=organization.id,
                contacts_csv_file=BytesIO(df.to_csv().encode("utf-8")),
            )


def test_import_contacts_list_with_null_columns(cleanup_database, cleanup_media):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    # fmt: off
    df = tribble(
        ["first_name", "last_name",       "email",       "role_title",   "location", "business_unit",],  # noqa: E241, E501
             "John",        None,      "JohnDoe@example.com",  "CEO",      "london-UK",   None,             # noqa: E241, E501, E131
    )
    # fmt: on
    with pytest.raises(
        ValidationException,
        match=re.escape(
            "(null) is/are not valid value for ['last_name', 'business_unit']."
        ),
    ):
        import_contact_list(
            organization_id=organization.id,
            contacts_csv_file=BytesIO(df.to_csv().encode("utf-8")),
        )


def test_import_contacts_list_with_invalid_email(cleanup_database, cleanup_media):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    unit = create_some_business_unit(organization_id=organization.id)
    assert isinstance(organization.id, int)
    # fmt: off
    df = tribble(
        ["first_name", "last_name",        "email",     "role_title", "location", "business_unit", ],  # noqa: E241, E501
             "John",         "Doe",         "JohnDoe@",      "CEO",      "london-UK",  f"{unit.id}-test",         # noqa: E241, E501, E131
    )
    # fmt: on
    with pytest.raises(
        ValidationException,
        match=re.escape("(JohnDoe@) is/are not valid value for Email."),
    ):
        import_contact_list(
            organization_id=organization.id,
            contacts_csv_file=BytesIO(df.to_csv().encode("utf-8")),
        )


def test_import_contacts_list_with_invalid_business_units(
    cleanup_database, cleanup_media
):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    create_some_business_unit(organization_id=organization.id)
    assert isinstance(organization.id, int)
    # fmt: off
    df = tribble(
        ["first_name", "last_name",      "email",       "role_title",   "location", "business_unit", ],  # noqa: E241, E501
               "John",      "Doe",   "JohnDoe@example.com",    "CEO",     "london-UK",   "invalid",  # noqa: E241, E501, E131
    )
    # fmt: on
    with pytest.raises(
        ValidationException,
        match=re.escape("(invalid) is/are not valid value for Business Unit."),
    ):
        import_contact_list(
            organization_id=organization.id,
            contacts_csv_file=BytesIO(df.to_csv().encode("utf-8")),
        )


def test_import_contacts_list_with_not_stored_business_units(
    cleanup_database, cleanup_media
):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    # fmt: off
    df = tribble(
        ["first_name", "last_name",      "email",       "role_title",   "location", "business_unit", ],  # noqa: E241, E501
               "John",      "Doe",   "JohnDoe@example.com",    "CEO",     "london-UK",       "1-test",             # noqa: E241, E501, E131
    )
    # fmt: on
    with pytest.raises(
        NotFoundException,
        match=re.escape("BusinessUnit with ID (1) not found."),
    ):
        import_contact_list(
            organization_id=organization.id,
            contacts_csv_file=BytesIO(df.to_csv().encode("utf-8")),
        )
