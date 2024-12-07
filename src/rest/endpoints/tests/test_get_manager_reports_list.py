from starlette.status import HTTP_200_OK

from entity import User
from repository.tests.helpers import (
    create_some_organization,
    create_some_business_unit,
    create_some_employee,
    create_some_management_position,
    create_some_report,
    publish_report,
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_get_manager_reports_list(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e.id, int)
    assert isinstance(bu.id, int)
    mp = create_some_management_position(
        manager_ids=[e.id],
        name="Test Position",
        role_ids=[bu.id],
        organization_id=org.id,
    )
    assert isinstance(mp.id, int)
    r = create_some_report(position_id=mp.id)
    assert isinstance(r.id, int)
    publish_report(report_id=r.id)
    assert isinstance(e.user, User)
    token = get_access_token(e.user)
    response = fast_client.get(
        URLs.manager_reports.format(id=e.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 1
    response_data = response.json()["result"]
    assert len(response_data) == 1
    item = response_data[0]
    assert isinstance(item["id"], int)
    assert isinstance(item["management_position"]["id"], int)
    assert isinstance(item["management_position"]["name"], str)
    assert item["management_position"]["id"] == mp.id
    assert item["management_position"]["name"] == mp.name
    assert item["id"] == r.id
