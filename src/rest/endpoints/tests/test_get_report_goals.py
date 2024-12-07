import httpx
from starlette.status import HTTP_200_OK
from entity import Employee, Report, User
from repository.tests.helpers import (
    create_some_organization,
    create_some_business_unit,
    create_some_employee,
    create_some_management_position,
    create_some_report,
    create_some_report_goal,
    publish_report,
)
from .helpers import get_access_token, get_admin_token, URLs
from settings import FocusArea


def _create_report_goals(publish: bool) -> tuple[Report, Employee]:
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
    create_some_report_goal(report_id=r.id, manager_id=e.id, title="Title1")
    create_some_report_goal(report_id=r.id, manager_id=e.id, title="Title2")
    if publish:
        publish_report(report_id=r.id)
    return r, e


def _assert_response_data(response: httpx.Response):
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert response.json()["total_count"] == 2
    assert isinstance(data, list) and len(data) == 2
    assert set(data[0].keys()) == {
        "id",
        "title",
        "manager_id",
        "description",
        "focus_area",
        "updated_at",
        "created_at",
    }


def test_get_report_goals(cleanup_database, fast_client, cleanup_media):
    report, employee = _create_report_goals(publish=True)
    assert isinstance(employee.user, User)
    manager_token = get_access_token(employee.user)
    response = fast_client.get(
        URLs.report_goals.format(id=report.id),
        headers=dict(Authorization=manager_token),
        params=dict(focus_area=FocusArea.readiness.value),
    )
    _assert_response_data(response)


def test_get_report_goals_as_admin(cleanup_database, fast_client, cleanup_media):
    report, _ = _create_report_goals(publish=False)
    admin_token = get_admin_token()
    response = fast_client.get(
        URLs.report_goals.format(id=report.id),
        headers=dict(Authorization=admin_token),
        params=dict(focus_area=FocusArea.readiness.value),
    )
    _assert_response_data(response)
