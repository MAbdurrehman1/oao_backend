from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_business_unit,
    create_some_management_position,
    create_some_organization,
    create_some_employee,
    create_some_report,
)
from .helpers import get_admin_token, URLs
from settings import configs


def test_get_organizaation_reports(
    fast_client, cleanup_database, cleanup_media, mock_post_request
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    assert isinstance(bu.id, int)
    e = create_some_employee(
        email="test@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e.id, int)
    mp = create_some_management_position(
        organization_id=org.id, manager_ids=[e.id], role_ids=[bu.id]
    )
    end_date = datetime.now() - timedelta(days=5)
    assert isinstance(mp.id, int)
    report = create_some_report(
        title="test title",
        end_date=end_date,
        position_id=mp.id,
    )
    token = get_admin_token()
    response = fast_client.get(
        URLs.organization_reports.format(id=org.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 1
    data = response.json()["result"][0]
    assert set(data.keys()) == {
        "id",
        "title",
        "end_date",
        "management_position",
        "status",
        "created_at",
        "updated_at",
    }
    assert set(data["management_position"].keys()) == {
        "id",
        "name",
    }
    assert isinstance(data["id"], int)
    assert data["id"] == report.id
    assert data["title"] == report.title
    assert data["end_date"] == end_date.strftime(configs.date_time_format)
    assert data["management_position"]["id"] == mp.id
    assert data["management_position"]["name"] == mp.name
    assert isinstance(
        datetime.strptime(data["created_at"], configs.date_time_format), datetime
    )
    assert isinstance(
        datetime.strptime(data["updated_at"], configs.date_time_format), datetime
    )
