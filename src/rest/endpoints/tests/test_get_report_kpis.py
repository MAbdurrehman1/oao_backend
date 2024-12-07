import httpx
from starlette.status import HTTP_200_OK

from entity import Employee, User, Report
from entity.kpi_entity import ReadinessKPI

from repository.tests.helpers import (
    create_some_organization,
    create_some_business_unit,
    create_some_employee,
    create_some_management_position,
    create_some_report,
    create_some_kpis,
    publish_report,
)
from rest.endpoints.tests.helpers import get_access_token, URLs, get_admin_token


def _create_report_kpis(publish: bool) -> tuple[Report, Employee]:
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
    create_some_kpis(report_id=r.id)
    if publish:
        publish_report(report_id=r.id)
    return r, e


def _assert_response_data(response: httpx.Response, length: int = 3):
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == length
    assert set(data[0].keys()) == {
        "id",
        "name",
        "report_id",
        "score",
        "standard_deviation",
        "created_at",
        "updated_at",
    }
    assert isinstance(response.json()["hierarchy"], dict)


def test_get_report_kpis(cleanup_database, fast_client, cleanup_media):
    report, employee = _create_report_kpis(publish=True)
    assert isinstance(employee.user, User)
    token = get_access_token(employee.user)
    response = fast_client.get(
        URLs.report_kpis.format(id=report.id), headers=dict(Authorization=token)
    )
    _assert_response_data(response)


def test_get_report_sub_kpis(cleanup_database, fast_client, cleanup_media):
    report, employee = _create_report_kpis(publish=True)
    assert isinstance(employee.user, User)
    token = get_access_token(employee.user)
    response = fast_client.get(
        URLs.report_kpis.format(id=report.id) + f"?parent_kpi={ReadinessKPI.name}",
        headers=dict(Authorization=token),
    )
    _assert_response_data(response, length=6)


def test_get_report_kpis_as_admin(cleanup_database, fast_client, cleanup_media):
    report, _ = _create_report_kpis(publish=False)
    token = get_admin_token()
    response = fast_client.get(
        URLs.report_kpis.format(id=report.id), headers=dict(Authorization=token)
    )
    _assert_response_data(response)
