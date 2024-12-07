from io import BytesIO

from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

from .helpers import (
    get_contacts_list_with_one_row_file,
    URLs,
    get_admin_token,
)
from repository.tests.helpers import (
    create_some_organization,
    create_some_business_unit,
)


def test_upload_contacts_list(fast_client, cleanup_database, cleanup_media):
    organization = create_some_organization()
    token = get_admin_token()
    assert isinstance(organization.id, int)
    business_unit = create_some_business_unit(
        name="test", organization_id=organization.id
    )
    assert isinstance(business_unit.id, int)
    file = get_contacts_list_with_one_row_file(business_unit.id)
    response = fast_client.post(
        url=URLs.upload_contacts_list,
        files=dict(file=file),
        params=dict(organization_id=organization.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Successful Contacts List Upload"}


def test_upload_contacts_list_with_invalid_file(fast_client, cleanup_database):
    invalid_file = (
        "contacts.csv",
        BytesIO("InvalidßContent".encode("latin1")),
        "text/csv",
    )
    organization = create_some_organization()
    token = get_admin_token()
    response = fast_client.post(
        url=URLs.upload_contacts_list,
        files=dict(file=invalid_file),
        params=dict(organization_id=organization.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "error": "Failed to process CSV File. please provide a valid CSV File"
    }
