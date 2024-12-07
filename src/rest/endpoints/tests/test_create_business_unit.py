from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from repository import BusinessUnitRepository
from repository.tests.helpers import (
    create_some_business_unit,
    create_some_organization,
)
from rest.endpoints.tests.helpers import URLs, get_admin_token


def test_create_business_unit_with_wrong_organization_id(
    cleanup_database, fast_client, cleanup_media
):
    data = dict(name="business unit name", parent_id=None)
    token = get_admin_token()
    response = fast_client.post(
        URLs.organization_business_units.format(id=0),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_404_NOT_FOUND


def test_create_business_unit_with_parent_id_not_belonging_to_organization_id(
    cleanup_database, fast_client, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    assert isinstance(bu.id, int)
    another_org = create_some_organization(
        logo_user_email="test2@example.ai", logo_name="sf.png"
    )
    assert isinstance(another_org.id, int)
    data = dict(name="business unit name", parent_id=bu.id)
    token = get_admin_token()
    response = fast_client.post(
        URLs.organization_business_units.format(id=another_org.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_create_business_unit(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    data = dict(name="business unit name", parent_id=None)
    token = get_admin_token()
    response = fast_client.post(
        URLs.organization_business_units.format(id=org.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Business Unit Created Successfully"}
    bus = BusinessUnitRepository.get_hierarchy(organization_id=org.id)
    assert len(bus) == 1
    assert bus[0].name == "business unit name"
    assert bus[0].parent_id is None

    child_data = dict(name="business unit child", parent_id=bus[0].id)
    response = fast_client.post(
        URLs.organization_business_units.format(id=org.id),
        headers=dict(Authorization=token),
        json=child_data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Business Unit Created Successfully"}
    bus = BusinessUnitRepository.get_hierarchy(organization_id=org.id)
    assert len(bus) == 2
    assert bus[1].name == "business unit child"
    assert bus[1].parent_id == bus[0].id
