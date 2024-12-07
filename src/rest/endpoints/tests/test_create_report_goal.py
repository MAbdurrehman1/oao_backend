from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_management_position,
    create_some_report,
    create_some_business_unit,
    publish_report,
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_create_report_goal(cleanup_database, fast_client, cleanup_media):
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
    data = dict(
        title="test title",
        description="test description",
        focus_area="READINESS",
    )
    manager_token = get_access_token(e.user)
    response = fast_client.post(
        URLs.report_goals.format(id=r.id),
        headers=dict(Authorization=manager_token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Report Goal Created Successfully"}
