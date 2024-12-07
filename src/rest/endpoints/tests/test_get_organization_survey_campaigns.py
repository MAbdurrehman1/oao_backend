from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
)
from .helpers import get_admin_token, URLs
from settings import configs


def test_update_survey_campaign(fast_client, cleanup_database, cleanup_media):
    org = create_some_organization()
    e = create_some_employee(email="test@example.com", organization_id=org.id)
    title = "test title"
    start_date = datetime.now() + timedelta(days=1)
    end_date = datetime.now() + timedelta(days=5)

    create_some_employee_survey_campaign(
        title=title,
        start_date=datetime.now() + timedelta(days=1),
        end_date=datetime.now() + timedelta(days=5),
        organization_id=org.id,
        participant_ids=[e.id],
    )
    token = get_admin_token()
    response = fast_client.get(
        URLs.organization_survey_campaigns.format(id=org.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 1
    data = response.json()["result"][0]
    assert isinstance(data["id"], int)
    assert data["title"] == title
    assert data["start_date"] == start_date.strftime(configs.date_time_format)
    assert data["end_date"] == end_date.strftime(configs.date_time_format)
    assert data["participants_count"] == 1
    assert data["invited_participants_count"] == 0
    assert data["responded_participants_count"] == 0
    assert isinstance(
        datetime.strptime(data["created_at"], configs.date_time_format), datetime
    )
    assert isinstance(
        datetime.strptime(data["updated_at"], configs.date_time_format), datetime
    )
