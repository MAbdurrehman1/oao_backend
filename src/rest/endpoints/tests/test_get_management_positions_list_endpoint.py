from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_business_unit,
    create_some_management_position,
)
from rest.endpoints.tests.helpers import get_admin_token, URLs


def assert_response_data(response_data: dict):
    for item in response_data:
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["managers_count"], int)
        assert isinstance(item["last_report_end_date"], str)
        assert isinstance(item["pending_participants_count"], int)
        assert isinstance(item["roles"], list)
        assert {"name", "id"} == set(item["roles"][0].keys())


def test_get_management_positions_list_endpoint(
    cleanup_database, fast_client, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e.id, int)
    assert isinstance(bu.id, int)
    create_some_management_position(
        manager_ids=[e.id],
        name="Test Position",
        role_ids=[bu.id],
        organization_id=org.id,
    )
    token = get_admin_token()
    response = fast_client.get(
        URLs.organization_management_positions.format(id=org.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 1
    assert_response_data(response.json()["result"])
