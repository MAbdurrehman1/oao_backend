from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    create_some_module,
    create_some_file,
)
from settings import configs
from .helpers import URLs, get_access_token


def test_upsert_module_schedule(
    cleanup_redis,
    cleanup_media,
    cleanup_database,
    mock_azure_requests,
    fast_client,
):
    file = create_some_file()
    assert isinstance(file.id, int)
    org = create_some_organization(logo_id=file.id)
    assert isinstance(org.id, int)
    e = create_some_employee(
        organization_id=org.id,
    )
    assert isinstance(e.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
    )
    assert isinstance(sc.id, int)
    m = create_some_module(
        still_thumbnail_id=file.id,
        animated_thumbnail_id=file.id,
    )
    assert isinstance(m.id, int)
    token = get_access_token(e.user)
    selected_date = datetime.now() + timedelta(days=1)
    response = fast_client.post(
        url=URLs.module_schedule.format(id=m.id),
        headers=dict(Authorization=token),
        json=dict(date=selected_date.strftime(configs.date_time_format)),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Module schedule created successfully."}
