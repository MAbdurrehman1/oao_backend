from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from repository import BusinessUnitRepository
from repository.tests.helpers import (
    create_some_business_unit,
    create_some_organization,
)
from rest.endpoints.tests.helpers import URLs, get_admin_token


def test_update_business_unit_with_wrong_organization_id(
    cleanup_database, fast_client, cleanup_media
):
    data = dict(name="business unit name", parent_id=None)
    token = get_admin_token()
    response = fast_client.put(
        URLs.organization_business_unit_update.format(o_id=0, bu_id=1),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_404_NOT_FOUND


def test_update_business_unit_with_parent_id_not_belonging_to_organization_id(
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
    response = fast_client.put(
        URLs.organization_business_unit_update.format(o_id=another_org.id, bu_id=bu.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_update_business_unit_not_belonging_to_organization_id(
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
    data = dict(name="business unit name", parent_id=None)
    token = get_admin_token()
    response = fast_client.put(
        URLs.organization_business_unit_update.format(o_id=another_org.id, bu_id=bu.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_404_NOT_FOUND


def test_update_business_unit_with_duplicated_root(
    cleanup_database, fast_client, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    root_bu = create_some_business_unit(
        name="root bu", parent_id=None, organization_id=org.id
    )
    assert isinstance(root_bu.id, int)
    bu = create_some_business_unit(
        name="child bu", parent_id=root_bu.id, organization_id=org.id
    )
    data = dict(name="business unit name", parent_id=None)
    token = get_admin_token()
    response = fast_client.put(
        URLs.organization_business_unit_update.format(o_id=org.id, bu_id=bu.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_update_business_unit_with_setting_child_as_parent(
    cleanup_database, fast_client, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    root_bu = create_some_business_unit(
        name="root bu", parent_id=None, organization_id=org.id
    )
    assert isinstance(root_bu.id, int)
    bu = create_some_business_unit(
        name="bu", parent_id=root_bu.id, organization_id=org.id
    )
    child_bu = create_some_business_unit(
        name="child bu", parent_id=bu.id, organization_id=org.id
    )
    data = dict(name="business unit name", parent_id=child_bu.id)
    token = get_admin_token()
    response = fast_client.put(
        URLs.organization_business_unit_update.format(o_id=org.id, bu_id=bu.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_update_business_unit(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(
        name="pre update", parent_id=None, organization_id=org.id
    )
    data = dict(name="business unit updated name", parent_id=None)
    token = get_admin_token()
    response = fast_client.put(
        URLs.organization_business_unit_update.format(o_id=org.id, bu_id=bu.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.json() == {"result": "Business Unit Updated Successfully"}
    assert response.status_code == HTTP_200_OK
    bus = BusinessUnitRepository.get_hierarchy(organization_id=org.id)
    assert len(bus) == 1
    assert bus[0].name == "business unit updated name"
    assert bus[0].parent_id is None

    child_bu = create_some_business_unit(
        name="child pre-update name", parent_id=bus[0].id, organization_id=org.id
    )
    child_update_data = dict(name="child post-update-name", parent_id=bus[0].id)
    response = fast_client.put(
        URLs.organization_business_unit_update.format(o_id=org.id, bu_id=child_bu.id),
        headers=dict(Authorization=token),
        json=child_update_data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Business Unit Updated Successfully"}
    bus = BusinessUnitRepository.get_hierarchy(organization_id=org.id)
    assert len(bus) == 2
    assert bus[1].name == "child post-update-name"
    assert bus[1].parent_id == bus[0].id
