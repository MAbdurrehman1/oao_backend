from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_module,
    create_some_employee,
    create_some_organization,
    create_some_employee_survey_campaign,
    create_some_file,
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_get_modules_list(cleanup_database, fast_client, cleanup_media):
    file = create_some_file()
    assert isinstance(file.id, int)
    [
        create_some_module(
            title=f"Test Title {i + 1}",
            order=i + 1,
            still_thumbnail_id=file.id,
            animated_thumbnail_id=file.id,
        )
        for i in range(3)
    ]
    org = create_some_organization(logo_id=file.id)
    e = create_some_employee(organization_id=org.id)
    create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
        start_date=datetime.now() - timedelta(days=2),
        end_date=datetime.now() + timedelta(days=5),
    )
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.module,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 3
    data = response.json()["result"]
    assert len(data) == 3
    assert set(data[0].keys()) == {
        "title",
        "description",
        "end_date",
        "duration",
        "order",
        "animated_thumbnail_url",
        "still_thumbnail_url",
        "id",
        "created_at",
        "updated_at",
    }
